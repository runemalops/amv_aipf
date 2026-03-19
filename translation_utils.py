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
                # Split comma/newline separated values
                raw_value = getattr(item, field, "")
                if raw_value:
                    item_dict[field] = raw_value.split(
                        "," if field == "technologies" else "\n"
                    )
                else:
                    item_dict[field] = []
            else:
                item_dict[field] = get_translated(item, field, lang)

        # Add non-translatable fields
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
