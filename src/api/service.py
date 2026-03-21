"""
Session background worker and metrics computation service.

SessionWorker:
  - Manages one asyncio.Task per active session
  - Every ~3 seconds inserts attendance, transcript, and speech metric rows
  - Prevents duplicate workers via an internal task registry
  - On stop: cancels the task, sets status to completed, generates a report

compute_metrics():
  - Aggregates data from attendance_metrics, speech_metrics tables
  - Returns MetricsResponse with computed scores
"""

import asyncio
import random
import logging
import json
from datetime import datetime
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import func

from src.api.models import (
    Session, AttendanceMetric, Transcript, SpeechMetric, SessionReport
)
from src.api.schemas import MetricsResponse, MetricsSummary, MetricsScores

logger = logging.getLogger("api.service")

# ---------------------------------------------------------------------------
# Sample data pools for realistic generation
# ---------------------------------------------------------------------------
SPEAKERS = [
    "Dr. Sarah Ahmed", "Student A", "Student B", "Student C",
    "Student D", "Teaching Assistant", "Student E", "Student F",
]

TRANSCRIPT_LINES = [
    "Let's begin today's lecture on supervised learning algorithms.",
    "Can you explain the difference between classification and regression?",
    "Great question. Classification predicts categories, regression predicts continuous values.",
    "The bias-variance tradeoff is fundamental to model selection.",
    "How do we decide which algorithm to use for a given problem?",
    "We evaluate using cross-validation and appropriate metrics.",
    "Let me show you an example with decision trees.",
    "Overfitting occurs when the model memorizes training data.",
    "Regularization helps prevent overfitting by adding a penalty term.",
    "Can you explain L1 versus L2 regularization?",
    "L1 produces sparse models, L2 distributes weights more evenly.",
    "Now let's look at ensemble methods like Random Forest.",
    "What is the advantage of bagging over a single decision tree?",
    "Bagging reduces variance by averaging multiple models.",
    "Gradient boosting builds trees sequentially to correct errors.",
    "Let's discuss the evaluation metrics: accuracy, precision, recall.",
    "Why is accuracy alone not sufficient for imbalanced datasets?",
    "F1 score provides a balance between precision and recall.",
    "Any more questions before we move to the practical exercise?",
    "Thank you, let's start coding the implementation now.",
]

QUESTION_LINES = {
    "Can you explain the difference between classification and regression?",
    "How do we decide which algorithm to use for a given problem?",
    "Can you explain L1 versus L2 regularization?",
    "What is the advantage of bagging over a single decision tree?",
    "Why is accuracy alone not sufficient for imbalanced datasets?",
    "Any more questions before we move to the practical exercise?",
}

KEY_TOPICS_POOL = [
    "Supervised Learning", "Classification vs Regression",
    "Bias-Variance Tradeoff", "Cross-Validation", "Decision Trees",
    "Overfitting & Regularization", "L1/L2 Regularization",
    "Ensemble Methods", "Random Forest", "Gradient Boosting",
    "Evaluation Metrics", "Precision/Recall/F1",
]


# ---------------------------------------------------------------------------
# Session Worker — manages background tasks
# ---------------------------------------------------------------------------

class SessionWorker:
    """Singleton-like manager for per-session background data generation tasks."""

    def __init__(self):
        self._tasks: dict[int, asyncio.Task] = {}
        self._transcript_index: dict[int, int] = {}
        logger.info("SessionWorker initialized")

    def is_running(self, session_id: int) -> bool:
        task = self._tasks.get(session_id)
        return task is not None and not task.done()

    async def start(self, session_id: int, db_factory):
        """
        Start the background data generation loop for a session.
        db_factory: a callable that returns a new DB session (SessionLocal).
        """
        if self.is_running(session_id):
            raise ValueError(f"Session {session_id} worker is already running")

        self._transcript_index[session_id] = 0
        task = asyncio.create_task(self._run_loop(session_id, db_factory))
        self._tasks[session_id] = task
        logger.info(f"Background worker STARTED for session {session_id}")

    async def stop(self, session_id: int, db_factory):
        """Cancel the background task, finalize the session, generate report."""
        task = self._tasks.get(session_id)
        if task and not task.done():
            task.cancel()
            try:
                await task
            except asyncio.CancelledError:
                pass
            logger.info(f"Background worker STOPPED for session {session_id}")

        self._tasks.pop(session_id, None)
        self._transcript_index.pop(session_id, None)

        # Finalize session in DB
        db = db_factory()
        try:
            session = db.query(Session).filter(Session.id == session_id).first()
            if session:
                session.status = "completed"
                session.end_time = datetime.utcnow()
                db.commit()
                logger.info(f"Session {session_id} marked as completed")

            # Generate report from collected data
            self._generate_report(session_id, db)
        finally:
            db.close()

    async def _run_loop(self, session_id: int, db_factory):
        """Background loop — inserts data every ~3 seconds."""
        base_attendance = random.randint(25, 45)
        tick = 0

        try:
            while True:
                db = db_factory()
                try:
                    tick += 1

                    # --- Attendance Metric ---
                    count = max(5, base_attendance + random.randint(-3, 3) - (tick // 10))
                    engagement = round(random.uniform(0.45, 0.95), 3)
                    db.add(AttendanceMetric(
                        session_id=session_id,
                        timestamp=datetime.utcnow(),
                        count=count,
                        engagement_score=engagement,
                    ))
                    logger.debug(f"[Session {session_id}] Attendance: count={count}, engagement={engagement}")

                    # --- Transcript ---
                    idx = self._transcript_index.get(session_id, 0)
                    line = TRANSCRIPT_LINES[idx % len(TRANSCRIPT_LINES)]
                    speaker = SPEAKERS[0] if line not in QUESTION_LINES else random.choice(SPEAKERS[1:])
                    is_q = line in QUESTION_LINES
                    db.add(Transcript(
                        session_id=session_id,
                        timestamp=datetime.utcnow(),
                        speaker=speaker,
                        text=line,
                        is_question=is_q,
                    ))
                    self._transcript_index[session_id] = idx + 1
                    logger.debug(f"[Session {session_id}] Transcript: [{speaker}] {line[:50]}...")

                    # --- Speech Metric ---
                    wpm = round(random.uniform(110.0, 175.0), 1)
                    silence_gap = round(random.uniform(0.5, 4.5), 2)
                    tone_var = round(random.uniform(0.15, 0.85), 3)
                    db.add(SpeechMetric(
                        session_id=session_id,
                        timestamp=datetime.utcnow(),
                        wpm=wpm,
                        silence_gap=silence_gap,
                        tone_variance=tone_var,
                    ))
                    logger.debug(f"[Session {session_id}] Speech: wpm={wpm}, gap={silence_gap}")

                    db.commit()
                except Exception as e:
                    db.rollback()
                    logger.error(f"[Session {session_id}] Data insertion error: {e}")
                finally:
                    db.close()

                await asyncio.sleep(3)

        except asyncio.CancelledError:
            logger.info(f"[Session {session_id}] Background loop cancelled")
            raise

    def _generate_report(self, session_id: int, db: DBSession):
        """Create a session_reports row summarizing the collected data."""
        try:
            attendance_rows = db.query(AttendanceMetric).filter(
                AttendanceMetric.session_id == session_id
            ).all()
            speech_rows = db.query(SpeechMetric).filter(
                SpeechMetric.session_id == session_id
            ).all()
            transcript_rows = db.query(Transcript).filter(
                Transcript.session_id == session_id
            ).all()

            if not attendance_rows:
                logger.warning(f"No data to generate report for session {session_id}")
                return

            avg_engagement = sum(r.engagement_score for r in attendance_rows) / len(attendance_rows)
            avg_wpm = sum(r.wpm for r in speech_rows) / len(speech_rows) if speech_rows else 0
            question_count = sum(1 for t in transcript_rows if t.is_question)
            total_lines = len(transcript_rows)
            interaction_ratio = question_count / total_lines if total_lines > 0 else 0

            overall = round((avg_engagement * 40) + (min(avg_wpm / 180, 1.0) * 30) + (interaction_ratio * 30), 1)

            topics = random.sample(KEY_TOPICS_POOL, min(5, len(KEY_TOPICS_POOL)))

            summary = (
                f"Session completed with {total_lines} transcript entries and "
                f"{len(attendance_rows)} attendance snapshots. "
                f"Average engagement was {avg_engagement:.2f}, "
                f"average speaking rate was {avg_wpm:.1f} WPM, and "
                f"{question_count} questions were asked."
            )

            report = SessionReport(
                session_id=session_id,
                summary=summary,
                key_topics=json.dumps(topics),
                overall_score=overall,
                created_at=datetime.utcnow(),
            )
            db.add(report)
            db.commit()
            logger.info(f"Report generated for session {session_id} — overall score: {overall}")
        except Exception as e:
            db.rollback()
            logger.error(f"Report generation error for session {session_id}: {e}")


# ---------------------------------------------------------------------------
# Metrics computation — reads from DB, returns computed aggregates
# ---------------------------------------------------------------------------

def compute_metrics(session_id: int, db: DBSession) -> MetricsResponse | None:
    """
    Query all related tables and compute aggregated metrics + scores.
    Returns None if the session does not exist.
    """
    session = db.query(Session).filter(Session.id == session_id).first()
    if not session:
        return None

    # --- Attendance aggregates ---
    attendance_rows = db.query(AttendanceMetric).filter(
        AttendanceMetric.session_id == session_id
    ).order_by(AttendanceMetric.timestamp).all()

    if attendance_rows:
        avg_engagement = round(sum(r.engagement_score for r in attendance_rows) / len(attendance_rows), 3)
        peak_attendance = max(r.count for r in attendance_rows)
        final_attendance = attendance_rows[-1].count
        dropoff_rate = round((peak_attendance - final_attendance) / peak_attendance * 100, 1) if peak_attendance > 0 else 0.0
    else:
        avg_engagement = 0.0
        peak_attendance = 0
        final_attendance = 0
        dropoff_rate = 0.0

    # --- Speech aggregates ---
    speech_rows = db.query(SpeechMetric).filter(
        SpeechMetric.session_id == session_id
    ).all()

    if speech_rows:
        avg_wpm = round(sum(r.wpm for r in speech_rows) / len(speech_rows), 1)
        avg_silence = round(sum(r.silence_gap for r in speech_rows) / len(speech_rows), 2)
        # silence_ratio: fraction of a 3-second window spent in silence
        silence_ratio = round(avg_silence / 3.0, 3)
    else:
        avg_wpm = 0.0
        silence_ratio = 0.0

    # --- Transcript stats for scoring ---
    total_transcripts = db.query(func.count(Transcript.id)).filter(
        Transcript.session_id == session_id
    ).scalar() or 0
    question_count = db.query(func.count(Transcript.id)).filter(
        Transcript.session_id == session_id,
        Transcript.is_question == True
    ).scalar() or 0
    interaction_ratio = question_count / total_transcripts if total_transcripts > 0 else 0

    # --- Compute scores (each 0-100) ---
    engagement_score = round(avg_engagement * 100, 1)
    clarity_score = round(min(avg_wpm / 180.0, 1.0) * 100 * (1 - silence_ratio * 0.3), 1)
    interaction_score = round(interaction_ratio * 100, 1)
    overall_score = round(
        engagement_score * 0.4 + clarity_score * 0.35 + interaction_score * 0.25, 1
    )

    return MetricsResponse(
        session_id=session_id,
        title=session.title,
        start_time=session.start_time,
        metrics=MetricsSummary(
            avg_engagement=avg_engagement,
            peak_attendance=peak_attendance,
            final_attendance=final_attendance,
            dropoff_rate=dropoff_rate,
            avg_wpm=avg_wpm,
            silence_ratio=silence_ratio,
        ),
        scores=MetricsScores(
            engagement=engagement_score,
            clarity=clarity_score,
            interaction=interaction_score,
            overall=overall_score,
        ),
    )


def compute_scores(session_id: int, db: DBSession) -> MetricsScores | None:
    """Compute only the scores portion (lighter query)."""
    result = compute_metrics(session_id, db)
    if result is None:
        return None
    return result.scores


# ---------------------------------------------------------------------------
# Global worker instance
# ---------------------------------------------------------------------------
worker = SessionWorker()
