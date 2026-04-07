def get_translated(obj, field, lang="en"):
    """
    Get translated value for a field.

    Args:
        obj: Database model instance with translations JSON column
        field: Field name to translate (e.g., 'title', 'description')
        lang: Target language code (default: 'en')

    Returns:
        Translated value or original if lang is 'en'
    """
    if lang == "en":
        return getattr(obj, field, "")

    translations = obj.translations or {}

    # Check if manual translation exists
    if lang in translations and field in translations[lang]:
        return translations[lang][field]

    # Fall back to original value (no auto-translation)
    return getattr(obj, field, "")


def get_translated_list(items, fields, lang="en"):
    """
    Get translated values for multiple items.

    Args:
        items: List of database model instances
        fields: List of field names to translate
        lang: Target language code

    Returns:
        List of dicts with translated values
    """
    result = []
    for item in items:
        item_dict = {}
        for field in fields:
            if field == "technologies" or field == "responsibilities":
                raw_value = getattr(item, field, "")
                if raw_value:
                    item_dict[field] = raw_value.split(
                        "," if field == "technologies" else "\n"
                    )
                else:
                    item_dict[field] = []
            else:
                item_dict[field] = get_translated(item, field, lang)

        if hasattr(item, "id"):
            item_dict["id"] = item.id
        if hasattr(item, "link"):
            item_dict["link"] = item.link or "#"
        if hasattr(item, "demo"):
            item_dict["demo"] = item.demo
        if hasattr(item, "git_url"):
            item_dict["git_url"] = item.git_url
        if hasattr(item, "git_icon"):
            item_dict["git_icon"] = item.git_icon
        if hasattr(item, "company"):
            item_dict["company"] = item.company
        if hasattr(item, "period"):
            item_dict["period"] = item.period
        if hasattr(item, "location"):
            item_dict["location"] = item.location or ""
        if hasattr(item, "image"):
            item_dict["image"] = item.image
        if hasattr(item, "date"):
            item_dict["date"] = item.date.strftime("%B %d, %Y") if item.date else ""
        if hasattr(item, "author"):
            item_dict["author"] = item.author
        if hasattr(item, "category"):
            item_dict["category"] = item.category
        if hasattr(item, "icon"):
            item_dict["icon"] = item.icon

        result.append(item_dict)

    return result


def get_education_list(educations, lang="en"):
    """
    Get translated education list.

    Args:
        educations: List of Education model instances
        lang: Target language code

    Returns:
        List of dicts with translated values
    """
    result = []
    for edu in educations:
        result.append(
            {
                "id": edu.id,
                "degree": get_translated(edu, "degree", lang),
                "school": get_translated(edu, "school", lang),
                "year": edu.year,
            }
        )
    return result


INTEREST_ICON_MAP = {
    "coding": "bi-code-square",
    "programming": "bi-code-square",
    "learning": "bi-book",
    "open source": "bi-github",
    "cloud computing": "bi-cloud",
    "machine learning": "bi-brain",
    "cybersecurity": "bi-shield-lock",
    "web development": "bi-globe",
    "mobile apps": "bi-phone",
    "music": "bi-music-note",
    "guitar": "bi-guitar",
    "motorcycles": "bi-bicycle",
    "cars": "bi-car-front",
    "racing": "bi-speedometer2",
    "videogames": "bi-controller",
    "gaming": "bi-controller",
    "pc gaming": "bi-pc-display",
    "photography": "bi-camera",
    "hiking": "bi-compass",
    "travel": "bi-airplane",
    "cooking": "bi-utensils",
    "reading": "bi-book",
    "writing": "bi-pen",
    "fitness": "bi-heart-pulse",
    "sports": "bi-dribbble",
    "coffee": "bi-cup-hot",
    "tea": "bi-cup",
    "movies": "bi-film",
    "series": "bi-tv",
    "anime": "bi-yin-yang",
    "art": "bi-palette",
    "design": "bi-palette",
}


def get_default_interest_icon(interest_name: str) -> str:
    name_lower = interest_name.lower()
    for key, icon in INTEREST_ICON_MAP.items():
        if key in name_lower or name_lower in key:
            return icon
    return "bi-heart"


def get_interests_list(interests, lang="en"):
    """
    Get translated interests list with icons.

    Args:
        interests: List of Interest model instances
        lang: Target language code

    Returns:
        List of dicts with name and icon
    """
    result = []
    for i in interests:
        name = get_translated(i, "name", lang)
        icon = i.icon if i.icon else get_default_interest_icon(name)
        result.append({"name": name, "icon": icon})
    return result


def get_social_links_list(links, lang="en"):
    """
    Get translated social links list.

    Args:
        links: List of SocialLink model instances
        lang: Target language code

    Returns:
        List of dicts with translated values
    """
    result = []
    for link in links:
        result.append(
            {
                "id": link.id,
                "platform": get_translated(link, "platform", lang),
                "url": link.url,
                "icon": link.icon,
            }
        )
    return result
