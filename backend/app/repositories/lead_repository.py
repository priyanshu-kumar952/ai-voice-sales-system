from app.core.database import pool
from app.models.lead import LeadCreate


class LeadRepository:
    @staticmethod
    def create(lead: LeadCreate):
        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO leads (
                        name,
                        phone,
                        budget,
                        preferred_location,
                        property_type
                    )
                    VALUES (%s, %s, %s, %s, %s)
                    RETURNING id, name, phone, budget,
                              preferred_location, property_type, created_at
                    """,
                    (
                        lead.name,
                        lead.phone,
                        lead.budget,
                        lead.preferred_location,
                        lead.property_type,
                    ),
                )

                row = cur.fetchone()

        return {
            "id": row[0],
            "name": row[1],
            "phone": row[2],
            "budget": row[3],
            "preferred_location": row[4],
            "property_type": row[5],
            "created_at": row[6],
        }