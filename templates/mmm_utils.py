"""
MMM-specific utilities for the spark-mmm extension plugin.

Requires ml_utils.py from the spark core plugin to be present
in the same directory (copied via Stage 0 of MMM commands).
"""

# --- Relevance Detection ---

MMM_KEYWORDS = {
    "spend", "cost", "impressions", "clicks", "media", "channel",
    "campaign", "ad", "marketing", "adstock", "cpm", "cpc", "ctr",
    "roas", "roi", "grp", "trp", "reach", "frequency",
}


def detect_mmm_relevance(source):
    """Check if a dataset has marketing/media columns suggesting MMM relevance.

    Args:
        source: list of column name strings, OR a dict (EDA report) with
                a 'columns' or 'column_types' key containing column names.

    Returns:
        dict with 'is_mmm': bool, 'matched_columns': list of matched column names
    """
    # Extract column names from various input formats
    if isinstance(source, dict):
        # EDA report format — try common keys
        column_names = (
            source.get("columns")
            or list(source.get("column_types", {}).get("numerical", []))
            + list(source.get("column_types", {}).get("categorical", []))
            or []
        )
    else:
        column_names = list(source)

    matched = []
    for col in column_names:
        col_lower = col.lower().replace("_", " ").replace("-", " ")
        for kw in MMM_KEYWORDS:
            if kw in col_lower:
                matched.append(col)
                break
    return {
        "is_mmm": len(matched) > 0,
        "matched_columns": matched,
    }


# --- Adstock Transformations ---

def compute_adstock(series, decay_rate=0.5):
    """Apply geometric adstock transformation to a media spend series.

    Args:
        series: array-like of spend values (ordered by time)
        decay_rate: float between 0 and 1 (higher = longer carryover)

    Returns:
        list of adstocked values
    """
    adstocked = [0.0] * len(series)
    adstocked[0] = float(series[0])
    for i in range(1, len(series)):
        adstocked[i] = float(series[i]) + decay_rate * adstocked[i - 1]
    return adstocked


# --- Contribution Decomposition ---

def decompose_contributions(coefficients, X_columns, X_means):
    """Compute channel contribution shares from model coefficients.

    Args:
        coefficients: dict of {channel_name: coefficient_value}
        X_columns: list of channel names
        X_means: dict of {channel_name: mean_value}

    Returns:
        dict of {channel_name: contribution_share} (sums to 1.0)
    """
    raw_contributions = {}
    for col in X_columns:
        if col in coefficients and col in X_means:
            raw_contributions[col] = abs(coefficients[col] * X_means[col])

    total = sum(raw_contributions.values())
    if total == 0:
        return {col: 0.0 for col in X_columns}

    return {col: val / total for col, val in raw_contributions.items()}
