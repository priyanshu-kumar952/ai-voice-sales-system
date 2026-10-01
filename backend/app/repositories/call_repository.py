from app.core.database import pool
from app.models.call import CallCreate, CallUpdate


class CallRepository:

    @staticmethod
    def create(call: CallCreate):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO calls (
                        call_id,
                        lead_id,
                        phone_number,
                        status
                    )
                    VALUES (%s, %s, %s, %s)
                    RETURNING
                        id,
                        call_id,
                        lead_id,
                        phone_number,
                        status,
                        started_at,
                        ended_at,
                        duration_seconds,
                        transcript,
                        created_at
                    """,
                    (
                        call.call_id,
                        call.lead_id,
                        call.phone_number,
                        call.status,
                    ),
                )

                row = cur.fetchone()

        return CallRepository._to_dict(row)

    @staticmethod
    def update(call_id: str, call: CallUpdate):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    UPDATE calls
                    SET
                        status = COALESCE(%s, status),
                        ended_at = COALESCE(%s, ended_at),
                        duration_seconds = COALESCE(
                            %s,
                            duration_seconds
                        ),
                        transcript = COALESCE(%s, transcript)
                    WHERE call_id = %s
                    RETURNING
                        id,
                        call_id,
                        lead_id,
                        phone_number,
                        status,
                        started_at,
                        ended_at,
                        duration_seconds,
                        transcript,
                        created_at
                    """,
                    (
                        call.status,
                        call.ended_at,
                        call.duration_seconds,
                        call.transcript,
                        call_id,
                    ),
                )

                row = cur.fetchone()

        if row is None:
            return None

        return CallRepository._to_dict(row)

    @staticmethod
    def _to_dict(row):
        return {
            "id": row[0],
            "call_id": row[1],
            "lead_id": row[2],
            "phone_number": row[3],
            "status": row[4],
            "started_at": row[5],
            "ended_at": row[6],
            "duration_seconds": row[7],
            "transcript": row[8],
            "created_at": row[9],
        }