import sys
from pathlib import Path

# Add project root to Python path
sys.path.append(str(Path(__file__).resolve().parent.parent))

from database.db_utils import get_all_scores, get_all_insights, get_average_scores


print("All Scores:")
print(get_all_scores())

print("\nInsights:")
print(get_all_insights())

print("\nAverage Scores:")
print(get_average_scores())