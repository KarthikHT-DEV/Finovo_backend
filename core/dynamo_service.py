"""
core/dynamo_service.py

DynamoDB caching layer for analytics projections.
Currently a no-op fallback — logs a warning so it's visible in CloudWatch.

To activate: implement real boto3 calls and use the EC2 IAM instance profile
for credentials (no access keys needed when running inside the VPC).
"""
import logging

logger = logging.getLogger(__name__)

class DynamoDBService:
    """Mock DynamoDB service — always falls back to RDS."""

    @staticmethod
    def get_projection(user_id, month_label):
        """Return None so the caller always recomputes from RDS."""
        logger.debug(
            "DynamoDB cache MISS (mock) — user=%s, label=%s",
            user_id,
            month_label,
        )
        return None

    @staticmethod
    def update_projection(user_id, month_label, start_date, end_date, response_data):
        """No-op — projection is NOT cached to DynamoDB."""
        logger.debug(
            "DynamoDB cache WRITE skipped (mock) — user=%s, label=%s",
            user_id,
            month_label,
        )
