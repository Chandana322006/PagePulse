def parse_page(data):
    if not data.get("title"):
        raise ValueError("Title missing")

    return {
        "title": data["title"],
        "links": len(data.get("links", []))
    }