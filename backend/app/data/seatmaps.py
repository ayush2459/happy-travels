def generate_seatmap(rows=30):

    seatmap = []

    for row in range(1, rows+1):

        seats = []

        for col in ["A","B","C","D","E","F"]:

            seats.append({
                "seat": f"{row}{col}",
                "available": True,
                "type": "WINDOW" if col in ["A","F"] else "AISLE" if col in ["C","D"] else "MIDDLE"
            })

        seatmap.append({
            "row": row,
            "seats": seats
        })

    return seatmap