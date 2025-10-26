def categorize_files(files):
    categories = {
        "school": ["assignment", "essay", "homework", "class"],
        "work": ["project", "report", "meeting", "invoice"],
        "personal": ["resume", "recipe", "journal", "budget"]
    }

    categorized = []
    counts = {}

    for file in files:
        name = file["name"].lower()
        category = "uncategorized"
        for cat, keywords in categories.items():
            if any(keyword in name for keyword in keywords):
                category = cat
                break
        categorized.append({"name": file["name"], "category": category})
        counts[category] = counts.get(category, 0) + 1

    return {
        "total_files": len(files),
        "categories": counts,
        "files": categorized
    }

def categorize_files_gemini(files):
    categories = {
        "school": ["assignment", "essay", "homework", "class"],
        "work": ["project", "report", "meeting", "invoice"],
        "personal": ["resume", "recipe", "journal", "budget"]
    }

    categorized = []
    counts = {}

    for file in files:
        name = file["name"].lower()
        category = "uncategorized"
        for cat, keywords in categories.items():
            if any(keyword in name for keyword in keywords):
                category = cat
                break
        categorized.append({"name": file["name"], "category": category})
        counts[category] = counts.get(category, 0) + 1

    return {
        "total_files": len(files),
        "categories": counts,
        "files": categorized
    }
