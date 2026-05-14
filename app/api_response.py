def success(data=None, meta=None):
    return {
        "success": True,
        "data": data,
        "meta": meta or {}
    }

def error(message, status=400):
    return {
        "success": False,
        "error": message,
        "status": status
    }