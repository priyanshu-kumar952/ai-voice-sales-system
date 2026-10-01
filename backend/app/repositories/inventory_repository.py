from app.core.database import pool


class InventoryRepository:
    @staticmethod
    def search(
        location: str | None = None,
        property_type: str | None = None,
        max_budget: int | None = None,
    ):
        query = """
            SELECT
                id,
                project_name,
                location,
                property_type,
                price,
                bedrooms,
                available_units
            FROM inventory
            WHERE available_units > 0
        """

        params = []

        if location:
            query += " AND location ILIKE %s"
            params.append(f"%{location}%")

        if property_type:
            query += " AND property_type ILIKE %s"
            params.append(f"%{property_type}%")

        if max_budget is not None:
            query += " AND price <= %s"
            params.append(max_budget)

        query += " ORDER BY price ASC"

        with pool.connection() as conn:
            with conn.cursor() as cur:
                cur.execute(query, params)
                rows = cur.fetchall()

        return [
            {
                "id": row[0],
                "project_name": row[1],
                "location": row[2],
                "property_type": row[3],
                "price": row[4],
                "bedrooms": row[5],
                "available_units": row[6],
            }
            for row in rows
        ]