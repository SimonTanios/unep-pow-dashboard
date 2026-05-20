from pathlib import Path
import ast
import html as html_lib
import re

import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html, dash_table, Input, Output, State, no_update
import dash_bootstrap_components as dbc

# ============================================================
# DATA PATHS
# ============================================================

DATA_DIR = Path("data")

# ============================================================
# INDICATOR CONFIGURATION
# ============================================================

INDICATORS = [
    {
        "id": "SP1.2",
        "tab_title": "SP1.2 Climate",
        "subprogramme": "SP1: Climate action",
        "short_name": "Climate policy adoption",
        "full_name": "Number of climate change mitigation, adaptation and disaster risk reduction strategies/policies/legal frameworks adopted",
        "period_file": DATA_DIR / "sp1_2_climate_country_period_summary.csv",
        "indicator_file": DATA_DIR / "sp1_2_climate_indicator_summary.csv",
        "docs_file": DATA_DIR / "sp1_2_climate_doc_level_deduped.csv",
        "main_score_candidates": ["SP1_2_Ci_t_UNEP", "Ci_t_UNEP"],
        "general_score_candidates": ["climate_policy_score"],
        "relevant_col_candidates": ["climate_relevant"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": ["evidence_of_unep_attributed_sp1_2_policy_adoption",
                                     "evidence_of_unep_attributed_sp1_2_policy_standard_action"],
        "extent_candidates": ["extent_of_unep_attributed_sp1_2_evidence"],
        "justification_candidates": ["climate_justification", "best_evidence_climate_justification"],
        "instrument_candidates": ["instrument_type", "best_evidence_instrument_type"],
        "general_metric_label": "Climate policy/legal framework score",
        "unep_metric_label": "UNEP-attributed climate policy evidence score",
    },
    {
        "id": "SP2.1",
        "tab_title": "SP2.1 Nature",
        "subprogramme": "SP2: Nature action: land, ocean and freshwater",
        "short_name": "Nature frameworks and instruments",
        "full_name": "Number of strengthened institutional and operational frameworks, policy and legal instruments, or positive incentives for sustainable and inclusive management of biodiversity and land, or prevention of ecosystem degradation",
        "period_file": DATA_DIR / "sp2_1_nature_country_period_summary.csv",
        "indicator_file": DATA_DIR / "sp2_1_nature_indicator_summary.csv",
        "docs_file": DATA_DIR / "sp2_1_nature_doc_level_deduped.csv",
        "main_score_candidates": ["SP2_1_Ci_t_UNEP", "Ci_t_UNEP"],
        "general_score_candidates": ["nature_framework_score"],
        "relevant_col_candidates": ["nature_relevant"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": ["evidence_of_unep_attributed_sp2_1_framework_strengthening"],
        "extent_candidates": ["extent_of_unep_attributed_sp2_1_evidence"],
        "justification_candidates": ["nature_justification", "best_evidence_nature_justification"],
        "instrument_candidates": ["nature_evidence_type", "best_evidence_type"],
        "general_metric_label": "Nature framework/instrument score",
        "unep_metric_label": "UNEP-attributed nature evidence score",
    },
    {
        "id": "SP3.1",
        "tab_title": "SP3.1 Chemicals & Pollution",
        "subprogramme": "SP3: Chemicals and pollution action",
        "short_name": "Policies, laws and regulations",
        "full_name": "Number of countries developing, adopting, revising or implementing policies, laws or regulations that advance circular approaches, sound management for chemicals and waste, and pollution prevention and control in key sectors",
        "period_file": DATA_DIR / "sp3_1_chemicals_pollution_country_period_summary.csv",
        "indicator_file": DATA_DIR / "sp3_1_chemicals_pollution_indicator_summary.csv",
        "docs_file": DATA_DIR / "sp3_1_chemicals_pollution_doc_level_deduped.csv",
        "main_score_candidates": ["SP3_1_Ci_t_UNEP", "Ci_t_UNEP"],
        "general_score_candidates": ["policy_regulation_score", "chemicals_policy_score", "pollution_policy_score",
                                     "policy_score"],
        "relevant_col_candidates": ["chemicals_relevant", "pollution_relevant", "policy_relevant"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": [
            "evidence_of_unep_attributed_sp3_1_policy_regulatory_action",
            "evidence_of_unep_attributed_sp3_1_policy_law_regulation",
            "evidence_of_unep_attributed_sp3_1_policy_action",
            "evidence_of_unep_attributed_sp3_1_evidence",
        ],
        "extent_candidates": ["extent_of_unep_attributed_sp3_1_evidence"],
        "justification_candidates": ["chemicals_justification", "pollution_justification", "policy_justification",
                                     "best_evidence_chemicals_justification"],
        "instrument_candidates": ["instrument_type", "best_evidence_instrument_type"],
        "general_metric_label": "Chemicals/pollution policy evidence score",
        "unep_metric_label": "UNEP-attributed chemicals/pollution evidence score",
    },
    {
        "id": "SP4.1",
        "tab_title": "SP4.1 Science-Policy Capacity",
        "subprogramme": "SP4: Science-policy",
        "short_name": "Environmental data and assessment capacity",
        "full_name": "Number of countries and institutions with strengthened capacity to develop environmental data, statistics, scientific reviews and assessments, and environmental data inputs",
        "period_file": DATA_DIR / "capacity_country_period_summary.csv",
        "indicator_file": DATA_DIR / "capacity_indicator_summary.csv",
        "docs_file": DATA_DIR / "capacity_doc_level_deduped.csv",
        "country_period_file": DATA_DIR / "country_capacity_period_summary_categorized.csv",
        "country_indicator_file": DATA_DIR / "country_capacity_indicator_summary.csv",
        "country_docs_file": DATA_DIR / "country_capacity_doc_level_deduped.csv",
        "main_score_candidates": ["Ci_t_UNEP", "SP4_1_Ci_t_UNEP"],
        "general_score_candidates": ["capacity_score", "cd"],
        "relevant_col_candidates": ["capacity_relevant", "capacity_evidence_doc"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": [
            "evidence_of_unep_attributed_capacity_strengthening",
            "evidence_of_unep_attributed_sp4_1_capacity_strengthening",
        ],
        "extent_candidates": ["extent_of_unep_attributed_capacity_evidence"],
        "justification_candidates": ["capacity_justification", "best_evidence_capacity_justification"],
        "instrument_candidates": ["capacity_evidence_type", "evidence_type"],
        "general_metric_label": "Country capacity evidence score",
        "unep_metric_label": "UNEP-attributed capacity evidence score",
    },
    {
        "id": "SP5.1",
        "tab_title": "SP5.1 Environmental Law",
        "subprogramme": "SP5: Environmental law and governance",
        "short_name": "Environmental law strengthening",
        "full_name": "Number of new policies or institutional support initiatives that contribute to strengthening environmental law in line with internationally agreed environmental objectives",
        "period_file": DATA_DIR / "sp5_1_env_law_country_period_summary.csv",
        "indicator_file": DATA_DIR / "sp5_1_env_law_indicator_summary.csv",
        "docs_file": DATA_DIR / "sp5_1_env_law_doc_level_deduped.csv",
        "main_score_candidates": ["SP5_1_Ci_t_UNEP", "Ci_t_UNEP"],
        "general_score_candidates": ["env_law_score", "environmental_law_score", "law_governance_score",
                                     "policy_support_score"],
        "relevant_col_candidates": ["env_law_relevant", "environmental_law_relevant", "law_governance_relevant"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": [
            "evidence_of_unep_attributed_sp5_1_environmental_law_strengthening",
            "evidence_of_unep_attributed_sp5_1_policy_support",
            "evidence_of_unep_attributed_sp5_1_evidence",
        ],
        "extent_candidates": ["extent_of_unep_attributed_sp5_1_evidence"],
        "justification_candidates": [
            "law_justification",
            "best_evidence_law_justification",
            "env_law_justification",
            "environmental_law_justification",
            "law_governance_justification",
            "best_evidence_env_law_justification",
        ],
        "instrument_candidates": ["instrument_type", "support_type", "best_evidence_instrument_type"],
        "general_metric_label": "Environmental law/policy support score",
        "unep_metric_label": "UNEP-attributed environmental law evidence score",
    },
    {
        "id": "SP6.1",
        "tab_title": "SP6.1 Finance & Economy",
        "subprogramme": "SP6: Finance and economic transformations",
        "short_name": "SCP, circularity and green economy instruments",
        "full_name": "Number of governments and public- and private-sector institutions that have adopted and/or taken action on policy instruments and/or standards accelerating the shift towards sustainable consumption and production, circularity and green economy approaches",
        "period_file": DATA_DIR / "sp6_1_finance_economic_country_period_summary.csv",
        "indicator_file": DATA_DIR / "sp6_1_finance_economic_indicator_summary.csv",
        "docs_file": DATA_DIR / "sp6_1_finance_economic_doc_level_deduped.csv",
        "main_score_candidates": ["SP6_1_Ci_t_UNEP", "Ci_t_UNEP"],
        "general_score_candidates": ["finance_policy_score"],
        "relevant_col_candidates": ["finance_relevant"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": ["evidence_of_unep_attributed_sp6_1_policy_standard_action"],
        "extent_candidates": ["extent_of_unep_attributed_sp6_1_evidence"],
        "justification_candidates": ["finance_justification", "best_evidence_finance_justification"],
        "instrument_candidates": ["instrument_type", "best_evidence_instrument_type"],
        "general_metric_label": "SCP/circularity/green economy score",
        "unep_metric_label": "UNEP-attributed SCP/circularity evidence score",
    },
    {
        "id": "SP7.1",
        "tab_title": "SP7.1 Digital",
        "subprogramme": "SP7: Digital transformations",
        "short_name": "Data management and sustainable AI",
        "full_name": "Measured improvements in data management and environmentally sustainable artificial intelligence practices, including capacity and skills development, among countries and stakeholders",
        "period_file": DATA_DIR / "sp7_1_digital_transformations_country_period_summary.csv",
        "indicator_file": DATA_DIR / "sp7_1_digital_transformations_indicator_summary.csv",
        "docs_file": DATA_DIR / "sp7_1_digital_transformations_doc_level_deduped.csv",
        "main_score_candidates": ["SP7_1_Ci_t_UNEP", "Ci_t_UNEP"],
        "general_score_candidates": ["digital_practice_score"],
        "relevant_col_candidates": ["digital_relevant"],
        "unep_flag_candidates": ["unep_attributed", "attributable_relevant_doc"],
        "unep_score_candidates": ["unep_attribution_score"],
        "evidence_flag_candidates": ["evidence_of_unep_attributed_sp7_1_digital_improvement"],
        "extent_candidates": ["extent_of_unep_attributed_sp7_1_evidence"],
        "justification_candidates": ["digital_justification", "best_evidence_digital_justification"],
        "instrument_candidates": ["improvement_type", "best_evidence_improvement_type"],
        "general_metric_label": "Data management / sustainable AI improvement score",
        "unep_metric_label": "UNEP-attributed digital transformation evidence score",
    },
]

OVERTON_42_FILE = DATA_DIR / "overton_42_government_unep_candidates.csv"


# ============================================================
# HELPERS
# ============================================================

def sid(text):
    """Safe id for Dash component IDs."""
    return str(text).replace(".", "_").replace(" ", "_").replace("-", "_").replace("/", "_")


def load_csv(path):
    if path and Path(path).exists():
        try:
            return pd.read_csv(path, encoding="utf-8-sig")
        except Exception:
            return pd.read_csv(path)
    return pd.DataFrame()


def clean_timewindow(df):
    if df is None or df.empty:
        return pd.DataFrame() if df is None else df

    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    if "TimeWindow" in df.columns:
        df["TimeWindow"] = (
            df["TimeWindow"]
            .astype(str)
            .str.strip()
            .str.replace("â€“", "-", regex=False)
            .str.replace("–", "-", regex=False)
            .str.replace("—", "-", regex=False)
            .str.replace("−", "-", regex=False)
        )

    if "Entity" in df.columns:
        df["Entity"] = (
            df["Entity"]
            .astype(str)
            .str.strip()
            .str.replace(r"\s+", " ", regex=True)
        )

    return df


def first_existing_col(df, candidates):
    if df is None or df.empty:
        return None
    for c in candidates:
        if c in df.columns:
            return c
    return None


def unique_cols(cols):
    seen = set()
    out = []
    for col in cols:
        if col and col not in seen:
            out.append(col)
            seen.add(col)
    return out


def bool_from_value(x):
    return str(x).strip().lower() in ["true", "1", "yes", "1.0"]


def safe_get(row, col, default=""):
    try:
        if col and col in row.index:
            value = row[col]
            if pd.isna(value):
                return default
            return value
    except Exception:
        pass
    return default


def get_numeric(value, default=0):
    try:
        if pd.isna(value):
            return default
        return float(value)
    except Exception:
        return default


def parse_evidence_phrases(value):
    if pd.isna(value):
        return []
    if isinstance(value, list):
        return value
    try:
        parsed = ast.literal_eval(str(value))
        if isinstance(parsed, list):
            return parsed
    except Exception:
        pass
    text = str(value).strip()
    return [text] if text else []


def prepare_download_text(lines):
    return "\n".join([str(x) for x in lines])


def classify_extent(score):
    score = get_numeric(score, 0)
    if score <= 0:
        return "no evidence"
    if score < 20:
        return "minimal evidence"
    if score < 40:
        return "low evidence"
    if score < 60:
        return "moderate evidence"
    if score < 80:
        return "strong evidence"
    return "very strong evidence"


def parse_year(value):
    if pd.isna(value):
        return None
    match = re.search(r"(20\d{2}|19\d{2})", str(value))
    return int(match.group(1)) if match else None


def assign_period_from_year(year):
    if pd.isna(year) or year is None:
        return "Unknown"
    year = int(year)
    if 2014 <= year <= 2018:
        return "2014-2018"
    if 2019 <= year <= 2022:
        return "2019-2022"
    if 2023 <= year <= 2026:
        return "2023-2026"
    return "Outside dashboard periods"


def data_table(df, page_size=10, style_extra=None):
    if df is None or df.empty:
        return dbc.Alert("No records available for the selected filters.", color="light")

    display_df = df.copy()

    # Avoid Dash DataTable JSON problems with lists/dicts/nans
    for col in display_df.columns:
        display_df[col] = display_df[col].apply(lambda x: "" if pd.isna(x) else str(x))

    style_cell = {
        "textAlign": "left",
        "fontFamily": "Arial",
        "fontSize": 13,
        "whiteSpace": "nowrap",
        "height": "38px",
        "minWidth": "120px",
        "maxWidth": "280px",
        "overflow": "hidden",
        "textOverflow": "ellipsis",
        "padding": "6px",
    }

    if style_extra:
        style_cell.update(style_extra)

    # Show full cell content on hover
    tooltip_data = [
        {
            column: {
                "value": str(value),
                "type": "text"
            }
            for column, value in row.items()
        }
        for row in display_df.to_dict("records")
    ]

    return html.Div(
        [
            html.Div(
                "Note: Hover over a cell to view the full content. Use the table filters and horizontal scroll to explore the evidence.",
                className="text-muted",
                style={"fontSize": "13px", "marginBottom": "6px"}
            ),

            dash_table.DataTable(
                columns=[{"name": c, "id": c} for c in display_df.columns],
                data=display_df.to_dict("records"),
                page_size=page_size,
                filter_action="native",
                sort_action="native",
                tooltip_data=tooltip_data,
                tooltip_duration=None,
                style_table={
                    "overflowX": "auto",
                    "maxHeight": "520px",
                    "overflowY": "auto",
                },
                style_cell=style_cell,
                style_header={
                    "fontWeight": "bold",
                    "backgroundColor": "#f8fafc",
                    "whiteSpace": "normal",
                    "height": "auto",
                    "border": "1px solid #d0d0d0",
                },
                style_data={
                    "height": "38px",
                    "maxHeight": "38px",
                    "border": "1px solid #e5e7eb",
                },
            ),
        ]
    )


def metric_card(title, value, subtitle=None):
    return dbc.Card(
        dbc.CardBody([
            html.Div(title, className="metric-title"),
            html.Div(str(value), className="metric-value"),
            html.Div(subtitle or "", className="metric-subtitle"),
        ]),
        className="metric-card h-100",
    )


def sp71_warning_wrapper(content):
    """
    Adds a strong warning banner and watermark to SP7.1 sections.
    Used because SP7.1 outputs require further validation and fine-tuning.
    """
    return html.Div(
        [
            dbc.Alert(
                [
                    html.Strong("Important notice — SP7.1 results: "),
                    html.Span(
                        "Fine-tuning with human-labelled data and prompt refinement "
                        "are strongly needed for this indicator."
                    ),
                ],
                color="danger",
                className="sp71-warning-banner",
            ),

            html.Div(
                [
                    html.Div("FINE-TUNING STRONGLY NEEDED", className="sp71-watermark-text"),
                    html.Div(content, className="sp71-content")
                ],
                className="sp71-watermark-wrapper",
            ),
        ]
    )


# ============================================================
# DATA PREPARATION
# ============================================================

def load_indicator_bundle(config):
    return {
        "period": clean_timewindow(load_csv(config["period_file"])),
        "indicator": clean_timewindow(load_csv(config["indicator_file"])),
        "docs": clean_timewindow(load_csv(config["docs_file"])),
        "country_period": clean_timewindow(load_csv(config.get("country_period_file", None))),
        "country_indicator": clean_timewindow(load_csv(config.get("country_indicator_file", None))),
        "country_docs": clean_timewindow(load_csv(config.get("country_docs_file", None))),
    }


def infer_periods(*dfs):
    periods = set()
    for df in dfs:
        if df is not None and not df.empty and "TimeWindow" in df.columns:
            periods.update(df["TimeWindow"].dropna().astype(str).str.strip().unique())
    return sorted([p for p in periods if p and p.lower() not in ["nan", "none"]])


def infer_entities(*dfs):
    entities = set()
    for df in dfs:
        if df is not None and not df.empty and "Entity" in df.columns:
            entities.update(df["Entity"].dropna().astype(str).str.strip().unique())
    return sorted([e for e in entities if e and e.lower() not in ["nan", "none"]])


def prepare_general_country_period_from_docs(config, docs):
    if docs.empty or "Entity" not in docs.columns or "TimeWindow" not in docs.columns:
        return pd.DataFrame()

    df = clean_timewindow(docs.copy())
    score_col = first_existing_col(df, config["general_score_candidates"])
    relevant_col = first_existing_col(df, config["relevant_col_candidates"])
    justification_col = first_existing_col(df, config["justification_candidates"])
    instrument_col = first_existing_col(df, config["instrument_candidates"])

    if not score_col:
        return pd.DataFrame()

    df[score_col] = pd.to_numeric(df[score_col], errors="coerce").fillna(0)

    if relevant_col:
        df = df[df[relevant_col].apply(bool_from_value)]

    df = df[df[score_col] > 0].copy()
    if df.empty:
        return pd.DataFrame()

    rows = []
    for (entity, time_window), group in df.groupby(["Entity", "TimeWindow"]):
        group = group.sort_values(score_col, ascending=False)
        best = group.iloc[0]
        rows.append({
            "Entity": entity,
            "TimeWindow": time_window,
            "general_score": round(group[score_col].mean(), 2),
            "max_general_score": round(group[score_col].max(), 2),
            "count_general_evidence_docs": len(group),
            "best_evidence_title": safe_get(best, "Title", "Untitled document"),
            "best_evidence_link": safe_get(best, "Link", ""),
            "best_evidence_type": safe_get(best, instrument_col, ""),
            "best_evidence_action_stage": safe_get(best, "action_stage", ""),
            "best_evidence_level": safe_get(best, "evidence_level", ""),
            "best_evidence_justification": safe_get(best, justification_col, ""),
            "best_evidence_unep_justification": safe_get(best, "unep_justification", ""),
            "best_evidence_phrases": safe_get(best, "evidence_phrases", "[]"),
        })

    return clean_timewindow(pd.DataFrame(rows).sort_values(["Entity", "TimeWindow"]))


def prepare_unep_country_period(config, period):
    if period.empty:
        return pd.DataFrame()

    df = clean_timewindow(period.copy())

    if "Entity" not in df.columns or "TimeWindow" not in df.columns:
        return pd.DataFrame()

    score_col = first_existing_col(df, config["main_score_candidates"])
    flag_col = first_existing_col(df, config["evidence_flag_candidates"])
    extent_col = first_existing_col(df, config["extent_candidates"])

    if score_col:
        df[score_col] = pd.to_numeric(df[score_col], errors="coerce").fillna(0)
        df["unep_score_for_app"] = df[score_col]
    else:
        df["unep_score_for_app"] = 0

    if flag_col:
        df["unep_evidence_flag_for_app"] = df[flag_col].apply(bool_from_value)
    else:
        df["unep_evidence_flag_for_app"] = df["unep_score_for_app"] > 0

    if extent_col:
        df["unep_extent_for_app"] = df[extent_col].astype(str)
    else:
        df["unep_extent_for_app"] = df["unep_score_for_app"].apply(classify_extent)

    return df


def normalize_general_period(config, bundle, docs_df):
    if not bundle["country_period"].empty:
        general_period = clean_timewindow(bundle["country_period"].copy())

        if "Ci_t_country_capacity" in general_period.columns:
            general_period["general_score"] = pd.to_numeric(general_period["Ci_t_country_capacity"],
                                                            errors="coerce").fillna(0)
        elif "general_score" not in general_period.columns:
            score_col = first_existing_col(general_period, config["general_score_candidates"])
            general_period["general_score"] = pd.to_numeric(general_period[score_col], errors="coerce").fillna(
                0) if score_col else 0

        if "count_capacity_evidence_docs" in general_period.columns:
            general_period["count_general_evidence_docs"] = general_period["count_capacity_evidence_docs"]
        elif "count_general_evidence_docs" not in general_period.columns:
            general_period["count_general_evidence_docs"] = 0

        if "best_evidence_capacity_justification" in general_period.columns and "best_evidence_justification" not in general_period.columns:
            general_period["best_evidence_justification"] = general_period["best_evidence_capacity_justification"]

        # Standardize best-evidence justification column across indicators
        if "best_evidence_justification" not in general_period.columns:
            possible_best_justification_cols = [
                "best_evidence_law_justification",
                "best_evidence_env_law_justification",
                "best_evidence_climate_justification",
                "best_evidence_nature_justification",
                "best_evidence_chemicals_justification",
                "best_evidence_finance_justification",
                "best_evidence_digital_justification",
                "best_evidence_capacity_justification",
                "law_justification",
                "env_law_justification",
            ]

            best_justification_col = first_existing_col(
                general_period,
                possible_best_justification_cols
            )

            if best_justification_col:
                general_period["best_evidence_justification"] = general_period[best_justification_col]

        country_docs_for_general = clean_timewindow(bundle["country_docs"])
    else:
        general_period = prepare_general_country_period_from_docs(config, docs_df)
        country_docs_for_general = docs_df.copy()

    return clean_timewindow(general_period), clean_timewindow(country_docs_for_general)


def filter_general_docs(config, docs, country, period):
    if docs.empty:
        return pd.DataFrame()

    df = clean_timewindow(docs.copy())
    if "Entity" not in df.columns or "TimeWindow" not in df.columns:
        return pd.DataFrame()

    df = df[
        (df["Entity"].astype(str).str.strip() == str(country).strip())
        & (df["TimeWindow"].astype(str).str.strip() == str(period).strip())
        ].copy()

    if df.empty:
        return df

    score_col = first_existing_col(df, config["general_score_candidates"])
    relevant_col = first_existing_col(df, config["relevant_col_candidates"])

    if relevant_col:
        df = df[df[relevant_col].apply(bool_from_value)]

    if score_col:
        df[score_col] = pd.to_numeric(df[score_col], errors="coerce").fillna(0)
        df = df[df[score_col] > 0].sort_values(score_col, ascending=False)

    return df


def filter_unep_docs(config, docs, country, period):
    if docs.empty:
        return pd.DataFrame()

    df = clean_timewindow(docs.copy())
    if "Entity" not in df.columns or "TimeWindow" not in df.columns:
        return pd.DataFrame()

    df = df[
        (df["Entity"].astype(str).str.strip() == str(country).strip())
        & (df["TimeWindow"].astype(str).str.strip() == str(period).strip())
        ].copy()

    if df.empty:
        return df

    attr_doc_col = "attributable_relevant_doc" if "attributable_relevant_doc" in df.columns else None
    unep_flag_col = first_existing_col(df, config["unep_flag_candidates"])

    if attr_doc_col:
        df = df[df[attr_doc_col].apply(bool_from_value)]
    elif unep_flag_col:
        df = df[df[unep_flag_col].apply(bool_from_value)]

    if "sd" in df.columns:
        df["sd"] = pd.to_numeric(df["sd"], errors="coerce").fillna(0)
        df = df[df["sd"] > 0].sort_values("sd", ascending=False)
    else:
        score_col = first_existing_col(df, config["unep_score_candidates"])
        if score_col:
            df[score_col] = pd.to_numeric(df[score_col], errors="coerce").fillna(0)
            df = df[df[score_col] > 0].sort_values(score_col, ascending=False)

    return df


def get_doc_score_cols(config, docs):
    contribution_col = "sd" if "sd" in docs.columns else None
    general_col = first_existing_col(docs, config["general_score_candidates"])
    unep_col = first_existing_col(docs, config["unep_score_candidates"])
    return contribution_col, general_col, unep_col


def parse_overton_42_data(df):
    if df.empty:
        return df

    df = df.copy()
    df.columns = [str(c).strip() for c in df.columns]

    needed_cols = [
        "Overton id", "Title", "Translated title", "Document type", "Source title",
        "Source country", "Source state", "Source sector", "Source organisation type",
        "Source function", "Published_on", "Policy citations (excl. same source)",
        "Policy citations (inc. same source)", "Document URL", "Overton URL",
        "Source specific tags", "Your tags", "Top topics", "Languages",
        "Policy authors", "Related to SDGs", "Document theme",
    ]

    for col in needed_cols:
        if col not in df.columns:
            df[col] = ""

    df["published_year"] = df["Published_on"].apply(parse_year)
    df["TimeWindow_42"] = df["published_year"].apply(assign_period_from_year)
    df["User_entity_42"] = df["Source title"].fillna("").astype(str)
    df["Entity_42"] = df["Source country"].fillna("").astype(str)
    df["SourceLayer"] = "Overton"
    df["indicator_42_candidate"] = True
    return df


bundles = {cfg["id"]: load_indicator_bundle(cfg) for cfg in INDICATORS}
overton_42_raw = load_csv(OVERTON_42_FILE)
overton_42 = parse_overton_42_data(overton_42_raw)

# Cache normalized per-indicator data in memory
PREPARED = {}
for cfg in INDICATORS:
    bundle = bundles[cfg["id"]]
    docs_df = clean_timewindow(bundle["docs"])
    period_df = prepare_unep_country_period(cfg, bundle["period"])
    general_period, country_docs_for_general = normalize_general_period(cfg, bundle, docs_df)
    PREPARED[cfg["id"]] = {
        "config": cfg,
        "bundle": bundle,
        "docs": docs_df,
        "period": period_df,
        "general_period": general_period,
        "country_docs_for_general": country_docs_for_general,
        "entities": infer_entities(period_df, docs_df, general_period),
        "periods": infer_periods(period_df, docs_df, general_period),
    }


# ============================================================
# SUMMARY HELPERS
# ============================================================

def find_indicator_value_column(indicator_df):
    if indicator_df.empty:
        return None

    preferred_patterns = [
        "number_entities_with", "number_countries_with", "number_governments",
        "governments_or_institutions", "countries_or_territories",
    ]
    for pattern in preferred_patterns:
        for col in indicator_df.columns:
            if pattern in str(col).lower():
                return col

    numeric_cols = indicator_df.select_dtypes(include="number").columns.tolist()
    for col in numeric_cols:
        if str(col).lower() not in ["period_midpoint", "total_entities_assessed"]:
            return col
    return None


def extract_latest_indicator_value(indicator_df):
    if indicator_df.empty:
        return "No data", "No data", "No data"

    df = indicator_df.copy()

    if "TimeWindow" in df.columns:
        df = df[~df["TimeWindow"].astype(str).isin(["Unknown", "Outside dashboard periods", "nan", "None", ""])]
    if df.empty:
        return "No data", "No data", "No data"

    if "TimeWindow" in df.columns:
        df["__sort_period"] = df["TimeWindow"].astype(str).str.extract(r"(\d{4})\D*$")[0]
        df["__sort_period"] = pd.to_numeric(df["__sort_period"], errors="coerce")
    elif "period_midpoint" in df.columns:
        df["__sort_period"] = pd.to_numeric(df["period_midpoint"], errors="coerce")
    else:
        df["__sort_period"] = range(len(df))

    df = df.sort_values("__sort_period", ascending=True)
    latest = df.iloc[-1]
    value_col = find_indicator_value_column(df)
    value = safe_get(latest, value_col, "No data") if value_col else "No data"

    if "TimeWindow" in latest.index:
        period = safe_get(latest, "TimeWindow", "Available data")
    elif "period_midpoint" in latest.index:
        period = safe_get(latest, "period_midpoint", "Available data")
    else:
        period = "Available data"

    return value, period, value_col or "No value column found"


def build_indicator_summary_df():
    rows = []
    for cfg in INDICATORS:
        p = PREPARED[cfg["id"]]
        period_df = p["period"]
        docs_df = p["docs"]
        general_period = p["general_period"]

        all_entities = set()
        all_periods = set()
        for df in [general_period, period_df, docs_df]:
            if not df.empty and "Entity" in df.columns:
                all_entities.update(df["Entity"].dropna().astype(str).unique())
            if not df.empty and "TimeWindow" in df.columns:
                all_periods.update(df["TimeWindow"].dropna().astype(str).unique())

        unep_country_periods = int(period_df[
                                       "unep_evidence_flag_for_app"].sum()) if not period_df.empty and "unep_evidence_flag_for_app" in period_df.columns else 0

        rows.append({
            "Subprogramme": cfg["subprogramme"],
            "Indicator": cfg["id"],
            "Short name": cfg["short_name"],
            "Countries/entities assessed": len(all_entities),
            "Periods assessed": len(all_periods),
            "Country-periods with general evidence": len(general_period) if not general_period.empty else 0,
            "Country-periods with UNEP-attributed evidence": unep_country_periods,
            "Data status": "Loaded" if not period_df.empty or not docs_df.empty else "Missing files",
        })
    return pd.DataFrame(rows)


def build_indicator_value_table():
    rows = []
    for cfg in INDICATORS:
        bundle = bundles[cfg["id"]]
        indicator_df = bundle.get("indicator", pd.DataFrame())
        value, period, value_source = extract_latest_indicator_value(indicator_df)

        if value == "No data":
            period_df = PREPARED[cfg["id"]]["period"]
            if not period_df.empty and "unep_evidence_flag_for_app" in period_df.columns:
                value = int(period_df["unep_evidence_flag_for_app"].sum())
                period = ", ".join(sorted(period_df["TimeWindow"].dropna().astype(str).unique()))
                value_source = "country-period UNEP-attributed evidence count"

        rows.append({
            "Subprogramme": cfg["subprogramme"],
            "Indicator": cfg["id"],
            "Short name": cfg["short_name"],
            "Prototype value": value,
            "Period / scope": period,
            "Countries/entities assessed in prototype": len(PREPARED[cfg["id"]]["entities"]),
            "Value source": "Latest-period UNEP-attributed country/entity count",
        })

    if overton_42 is not None and not overton_42.empty:
        valid_42 = overton_42[
            ~overton_42["TimeWindow_42"].astype(str).isin(["Outside dashboard periods", "Unknown", "nan", "None", ""])
        ].copy()
        if not valid_42.empty:
            period_summary_42 = (
                valid_42.groupby("TimeWindow_42")
                .agg(
                    governments_or_institutions=("User_entity_42", "nunique"),
                    countries_or_territories=("Entity_42", "nunique"),
                    candidate_documents=("Overton id", "count"),
                )
                .reset_index()
            )
            period_summary_42["__sort_period"] = pd.to_numeric(
                period_summary_42["TimeWindow_42"].astype(str).str.extract(r"(\d{4})\D*$")[0],
                errors="coerce",
            )
            latest = period_summary_42.sort_values("__sort_period").iloc[-1]
            rows.append({
                "Subprogramme": "SP4: Science-policy",
                "Indicator": "SP4.2",
                "Short name": "Use of UNEP knowledge, data and assessments",
                "Prototype value": safe_get(latest, "governments_or_institutions", 0),
                "Period / scope": safe_get(latest, "TimeWindow_42", "Available data"),
                "Countries/entities assessed in prototype": int(valid_42["Entity_42"].nunique()),
                "Value source": "Overton candidate government/institution count",
            })

    return pd.DataFrame(rows)


def build_scope_table():
    rows = []
    for cfg in INDICATORS:
        p = PREPARED[cfg["id"]]
        entities = p["entities"]
        periods = p["periods"]

        rows.append({
            "Subprogramme": cfg["subprogramme"],
            "Indicator": cfg["id"],
            "Indicator full name": cfg["full_name"],
            "Short name": cfg["short_name"],
            "Countries/entities assessed": f"{len(entities)} countries/entities assessed in the current prototype: {', '.join(entities[:20])}{'...' if len(entities) > 20 else ''}" if entities else "No country/entity data loaded for this indicator.",
            "Periods covered": ", ".join(periods) if periods else "No period data loaded.",
            "Methodology note": "AI-supported evidence harvesting, classification, scoring and aggregation workflow.",
        })

    if overton_42 is not None and not overton_42.empty:
        valid_42 = overton_42[overton_42["TimeWindow_42"] != "Outside dashboard periods"].copy()
        periods_42 = sorted([
            p for p in valid_42["TimeWindow_42"].dropna().astype(str).unique()
            if p not in ["Unknown", "Outside dashboard periods", "nan", "None", ""]
        ])
        rows.append({
            "Subprogramme": "SP4: Science-policy",
            "Indicator": "SP4.2",
            "Indicator full name": "Number of governments and institutions using UNEP-provided data, statistics and scientific assessments to catalyse policymaking and action",
            "Short name": "Use of UNEP knowledge, data and assessments",
            "Countries/entities assessed": (
                "All countries available within the Overton search/database scope. "
                f"The current export includes {len(valid_42)} candidate documents, "
                f"{valid_42['Entity_42'].dropna().astype(str).nunique()} countries/territories represented in the export, "
                f"and {valid_42['User_entity_42'].dropna().astype(str).nunique()} government/public-sector institutions."
            ),
            "Periods covered": ", ".join(periods_42) if periods_42 else "No period data loaded.",
            "Methodology note": "For this indicator, the custom algorithmic search and evidence-harvesting engine has not yet been applied. The current results rely on the Overton candidate evidence export only.",
        })
    return pd.DataFrame(rows)


# ============================================================
# FIGURE HELPERS
# ============================================================

def empty_fig(message="No data available"):
    fig = px.scatter()
    fig.update_layout(
        height=380,
        xaxis={"visible": False},
        yaxis={"visible": False},
        annotations=[{"text": message, "xref": "paper", "yref": "paper", "showarrow": False, "font": {"size": 16}}],
    )
    return fig


def assessed_map_fig(entities, title):
    if not entities:
        return empty_fig("No countries/entities available for mapping.")
    map_base = pd.DataFrame({"Entity": entities, "assessed": "Assessed"})
    fig = px.choropleth(
        map_base,
        locations="Entity",
        locationmode="country names",
        color="assessed",
        hover_name="Entity",
        title=title,
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True), height=560, margin=dict(l=0, r=0, t=50, b=0))
    return fig


def score_map_fig(df, value_col, title, color_scale="Viridis"):
    if df is None or df.empty or value_col not in df.columns:
        return empty_fig("No data available for the selected period.")
    fig = px.choropleth(
        df,
        locations="Entity",
        locationmode="country names",
        color=value_col,
        hover_name="Entity",
        hover_data=[c for c in
                    ["TimeWindow", value_col, "count_general_evidence_docs", "count_attributable_docs_nonzero_unep",
                     "best_evidence_title"] if c in df.columns],
        color_continuous_scale=color_scale,
        range_color=[0, 100],
        title=title,
    )
    fig.update_layout(geo=dict(showframe=False, showcoastlines=True), height=560, margin=dict(l=0, r=0, t=50, b=0))
    return fig


# ============================================================
# LAYOUT BUILDERS
# ============================================================

def executive_layout():
    summary_df = build_indicator_summary_df()
    value_table = build_indicator_value_table()
    scope_table = build_scope_table()

    fig_general = px.bar(
        summary_df,
        x="Indicator",
        y="Country-periods with general evidence",
        color="Subprogramme",
        text="Country-periods with general evidence",
        title="General evidence by indicator",
    )

    fig_unep = px.bar(
        summary_df,
        x="Indicator",
        y="Country-periods with UNEP-attributed evidence",
        color="Subprogramme",
        text="Country-periods with UNEP-attributed evidence",
        title="UNEP-attributed evidence by indicator",
    )

    return html.Div([
        html.H1("🌍 UNEP Programme of Work Indicator Evidence Dashboard"),
        dcc.Markdown(
            """
This dashboard brings together AI-supported evidence harvesting outputs for selected indicators under the
[UNEP Programme of Work 2026–2027](https://docs.un.org/en/UNEP/EA.7/4), across several UNEP subprogrammes.
It is designed to help subprogramme coordinators and other stakeholders see how the indicators can be supported
by an automated workflow for evidence discovery, classification, validation and visualization, to strengthen
results monitoring, evidence-based reporting, learning and communication under the UNEP Programme of Work 2026–2027.

This is a **basic prototype / proof of concept**. Further optimization, scale-up, validation, prompt refinement,
human-labelled datasets, model fine-tuning and workflow improvements can be implemented to improve accuracy,
coverage, usability and institutional uptake, including by expanding the historical period covered, increasing
country coverage, broadening multilingual search and evidence harvesting, and enabling features for ad hoc analyses and
real-time monitoring of selected Programme of Work indicators.

The dashboard separates:

- **general country/institution evidence**, where available from the harvested documents (for example, a national climate policy, biodiversity strategy, or legal framework adopted by a country, even if UNEP is not mentioned); and
- **UNEP-attributed evidence**, where the workflow identified an explicit link to UNEP support or contribution.
            """
        ),
        html.H3("Prototype coverage"),
        dbc.Row([
            dbc.Col(metric_card("Subprogrammes represented", summary_df["Subprogramme"].nunique()), md=6),
            dbc.Col(metric_card("Indicators covered", len(INDICATORS) + 1), md=6),
        ], className="g-3 mb-3"),
        dbc.Accordion([
            dbc.AccordionItem(data_table(scope_table, page_size=20),
                              title="Show prototype country/entity scope by indicator")
        ], start_collapsed=True, className="mb-4"),
        html.H3("Prototype indicator values based on the current analysis"),

        html.P(
            "The table below shows the latest available prototype value for each indicator view, "
            "based on the loaded analysis files. These values should be reviewed as prototype evidence outputs, "
            "not final official PoW reporting figures."
        ),

        html.Div(
            [
                html.Div("↓", className="prototype-arrow-symbol"),
                html.Div(
                    [
                        html.Strong("Focus on the Prototype value column. "),
                        html.Span(
                            "These are the indicative values that would be reported under the selected PoW indicators, "
                            "taking into account the current prototype limitations, data coverage, validation status "
                            "and methodological assumptions."
                        ),
                    ]
                ),
            ],
            className="prototype-callout-box",
        ),

        dash_table.DataTable(
            columns=[{"name": c, "id": c} for c in value_table.columns],
            data=value_table.fillna("").astype(str).to_dict("records"),
            page_size=20,
            style_table={"overflowX": "auto"},
            style_header={
                "fontWeight": "bold",
                "backgroundColor": "#f8fafc",
            },
            style_header_conditional=[
                {
                    "if": {"column_id": "Prototype value"},
                    "backgroundColor": "#fee2e2",
                    "color": "#991b1b",
                    "fontWeight": "800",
                    "borderTop": "4px solid #dc2626",
                    "borderLeft": "4px solid #dc2626",
                    "borderRight": "4px solid #dc2626",
                }
            ],
            style_data_conditional=[
                {
                    "if": {"column_id": "Prototype value"},
                    "backgroundColor": "#fff1f2",
                    "color": "#7f1d1d",
                    "fontWeight": "800",
                    "borderLeft": "4px solid #dc2626",
                    "borderRight": "4px solid #dc2626",
                },
                {
                    "if": {
                        "column_id": "Prototype value",
                        "row_index": len(value_table) - 1,
                    },
                    "borderBottom": "4px solid #dc2626",
                },
            ],
            style_cell={
                "textAlign": "left",
                "whiteSpace": "normal",
                "height": "auto",
                "fontSize": 13,
                "padding": "8px",
            },
        ),
        html.Hr(),
        html.H3("Subprogramme indicators covered"),
        data_table(summary_df, page_size=20),
        html.Hr(),
        html.H3("Summary by indicator"),
        html.P(
            "Note: the charts show country-period counts across all loaded periods, while the Prototype value table above shows the latest available period only.",
            className="text-muted"),
        dbc.Row([
            dbc.Col(dcc.Graph(figure=fig_general), md=6),
            dbc.Col(dcc.Graph(figure=fig_unep), md=6),
        ], className="g-3"),
    ])


def methodology_layout():
    expected_rows = []
    for cfg in INDICATORS:
        expected_rows.append({
            "Indicator": cfg["id"],
            "Country-period summary": str(cfg["period_file"]),
            "Indicator summary": str(cfg["indicator_file"]),
            "Document-level evidence": str(cfg["docs_file"]),
        })
    expected_rows.append({
        "Indicator": "SP4.2",
        "Country-period summary": "Not applicable currently",
        "Indicator summary": "Not applicable currently",
        "Document-level evidence": str(OVERTON_42_FILE),
    })

    return html.Div([
        html.H2("📘 Methodology"),
        dcc.Markdown(
            """
### 1. Purpose

The dashboard provides a common evidence-review interface for selected indicators under the
[UNEP Programme of Work 2026–2027](https://docs.un.org/en/UNEP/EA.7/4).
It is intended to support results communication, indicator tracking and evidence review across subprogrammes.

### 2. Evidence harvesting and classification workflow

For most indicators, the pipeline follows this workflow:

1. Define the indicator logic, evidence taxonomy, country/entity scope and time windows.
2. Harvest candidate evidence through structured web queries.
3. Harvest webpages and PDFs into text files.
4. Reduce long documents to fit the LLM context window.
5. Use an LLM to classify documents against the indicator definition.
6. Score both the indicator evidence and UNEP attribution evidence.
7. Deduplicate documents and aggregate to country-period and indicator-level outputs.
8. Visualize results and preserve an evidence audit trail.

### 3. General evidence versus UNEP-attributed evidence

**General evidence** reflects whether a document contains relevant evidence for the indicator,
regardless of whether UNEP is explicitly linked to the result.

**UNEP-attributed evidence** requires an explicit link between UNEP support/contribution and the
relevant indicator outcome. Mere mention of UNEP, a logo, author affiliation or bibliography-only
citation is not sufficient.

### 4. Document-level contribution score

For the AI-classified indicators, the document-level UNEP-attributed contribution score is generally:

`indicator evidence score × UNEP attribution score / 100`

The country-period UNEP-attributed score is then calculated from the relevant document-level contribution scores.

### 5. Indicator 4.2 exception

For Indicator 4.2, the current prototype uses evidence records obtained from the Overton platform. Although the workflow developed for this prototype includes its own algorithmic search and evidence-harvesting engine, Overton was used for this indicator at this stage for testing and comparison. The records come from government/public-sector policy sources connected to UNEP through citation or mention.

### 6. Interpretation note

These outputs reflect documented evidence found through the harvesting process. They should not be read as complete independent measurements of country performance, national capacity or UNEP impact. Further scale-up and triangulation are recommended to strengthen the robustness of the results, including through additional evidence sources, expert document labelling, validation against programme knowledge, and, where appropriate, the developement of a complementary data workflow that considers internal UNEP documents to complement publicly available evidence.
            """
        ),
        html.H3("Expected data files"),

        html.P(
            [
                "Note: View these files on ",
                html.A(
                    "GitHub/SimonTanios",
                    href="https://github.com/SimonTanios",
                    target="_blank"
                ),
                ". The files listed below are the expected input files used by the prototype dashboard."
            ],
            className="text-muted"
        ),

        data_table(pd.DataFrame(expected_rows), page_size=20),
    ])


def indicator_layout(cfg):
    p = PREPARED[cfg["id"]]
    prefix = sid(cfg["id"])

    period_options = [{"label": x, "value": x} for x in p["periods"]]
    entity_options = [{"label": x, "value": x} for x in p["entities"]]

    default_period = p["periods"][0] if p["periods"] else None
    default_entity = p["entities"][0] if p["entities"] else None

    return html.Div([
        html.H2(f"{cfg['subprogramme']} — {cfg['id']} {cfg['short_name']}"),
        html.P([html.B("Indicator: "), cfg["full_name"]]),

        dcc.Tabs(
            id=f"{prefix}-section-tabs",
            value="map",
            children=[
                dcc.Tab(label=f"{cfg['id']} Assessed Map", value="map"),
                dcc.Tab(label=f"{cfg['id']} Country/Institution Evidence", value="general"),
                dcc.Tab(label=f"{cfg['id']} UNEP-attributed Evidence", value="unep"),
                dcc.Tab(label=f"{cfg['id']} Country-Period Report", value="report"),
                dcc.Tab(label=f"{cfg['id']} Evidence Explorer", value="explorer"),
            ],
            className="mb-3",
        ),

        html.Div(id=f"{prefix}-section-content"),

        # Hidden stores for defaults and option data
        dcc.Store(id=f"{prefix}-default-period", data=default_period),
        dcc.Store(id=f"{prefix}-default-entity", data=default_entity),
        dcc.Store(id=f"{prefix}-period-options", data=period_options),
        dcc.Store(id=f"{prefix}-entity-options", data=entity_options),
    ])


def overton_42_layout():
    if overton_42.empty:
        return dbc.Alert("No Indicator 4.2 data found. Please add data/overton_42_government_unep_candidates.csv",
                         color="warning")

    valid = overton_42[
        ~overton_42["TimeWindow_42"].astype(str).isin(["Outside dashboard periods", "Unknown", "nan", "None", ""])
    ].copy()

    periods = sorted(valid["TimeWindow_42"].dropna().astype(str).unique()) if not valid.empty else []
    countries = sorted(valid["Entity_42"].dropna().astype(str).unique()) if not valid.empty else []

    return html.Div([
        html.H2("SP4: Science-policy — Indicator 4.2 Knowledge Use"),
        dcc.Markdown(
            """
**Indicator 4.2:** Number of governments and institutions that use UNEP knowledge,
data, statistics and scientific assessments to catalyse policymaking and action.

This section uses the candidate evidence export as a **candidate evidence base**. The records
come from government/public-sector sources connected to UNEP through citation or mention.

These results should be interpreted as **candidate evidence**, not yet as a final validated official count.
            """
        ),
        dcc.Tabs(
            id="sp42-tabs",
            value="overview",
            children=[
                dcc.Tab(label="Indicator 4.2 Overview", value="overview"),
                dcc.Tab(label="Indicator 4.2 Map", value="map"),
                dcc.Tab(label="Indicator 4.2 Evidence Report", value="report"),
            ],
            className="mb-3",
        ),
        html.Div(id="sp42-content"),
        dcc.Store(id="sp42-periods", data=[{"label": p, "value": p} for p in periods]),
        dcc.Store(id="sp42-countries", data=[{"label": c, "value": c} for c in countries]),
    ])


# ============================================================
# APP INITIALIZATION
# ============================================================

app = Dash(
    __name__,
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True,
    title="UNEP PoW Indicator Evidence Dashboard",
)

server = app.server

app.layout = dbc.Container(
    fluid=True,
    children=[

        dcc.Tabs(
            id="top-tabs",
            value="Executive Overview",
            children=[
                dcc.Tab(label="Executive Overview", value="Executive Overview"),
                dcc.Tab(label="Methodology", value="Methodology"),
                *[dcc.Tab(label=cfg["tab_title"], value=cfg["id"]) for cfg in INDICATORS],
                dcc.Tab(label="SP4.2 Knowledge Use", value="SP4.2"),
            ],
        ),

        html.Div(id="top-content", className="main-content"),
    ],
)


# ============================================================
# TOP-LEVEL CALLBACK
# ============================================================

@app.callback(Output("top-content", "children"), Input("top-tabs", "value"))
def render_top_tab(tab):
    if tab == "Executive Overview":
        return executive_layout()
    if tab == "Methodology":
        return methodology_layout()
    if tab == "SP4.2":
        return overton_42_layout()

    cfg = next((c for c in INDICATORS if c["id"] == tab), None)
    if cfg:
        return indicator_layout(cfg)

    return dbc.Alert("Unknown tab selected.", color="danger")


# ============================================================
# INDICATOR SECTION CALLBACKS
# ============================================================

def make_indicator_callbacks(cfg):
    prefix = sid(cfg["id"])

    @app.callback(
        Output(f"{prefix}-section-content", "children"),
        Input(f"{prefix}-section-tabs", "value"),
        prevent_initial_call=False,
    )
    def render_section(section):
        p = PREPARED[cfg["id"]]

        is_sp71 = cfg["id"] == "SP7.1"

        if not p["entities"] and not p["periods"]:
            return dbc.Alert("No data found for this indicator. Please add the expected CSV files to the data/ folder.",
                             color="warning")

        if section == "map":
            section_content = html.Div([
                html.H4(f"🗺️ {cfg['id']} Countries/Entities Assessed Map"),
                dcc.Graph(figure=assessed_map_fig(p["entities"],
                                                  f"{cfg['id']} countries/entities included in the assessment")),
                data_table(pd.DataFrame({"Entity": p["entities"], "assessed": "Assessed"}), page_size=20),
            ])
            return sp71_warning_wrapper(section_content) if is_sp71 else section_content

        if section == "general":
            opts = [{"label": x, "value": x} for x in
                    sorted(p["general_period"]["TimeWindow"].dropna().astype(str).unique())] if not p[
                "general_period"].empty and "TimeWindow" in p["general_period"].columns else []
            default = opts[0]["value"] if opts else None
            section_content = html.Div([
                html.H4(f"📊 {cfg['id']} Country/Institution Evidence — {cfg['short_name']}"),
                dbc.Row([
                    dbc.Col([
                        html.Label(f"Select {cfg['id']} period"),
                        dcc.Dropdown(id=f"{prefix}-general-period", options=opts, value=default, clearable=False),
                    ], md=4),
                ], className="mb-3"),
                html.Div(id=f"{prefix}-general-content"),
            ])
            return sp71_warning_wrapper(section_content) if is_sp71 else section_content

        if section == "unep":
            opts = [{"label": x, "value": x} for x in
                    sorted(p["period"]["TimeWindow"].dropna().astype(str).unique())] if not p[
                "period"].empty and "TimeWindow" in p["period"].columns else []
            default = opts[0]["value"] if opts else None
            section_content = html.Div([
                html.H4(f"🌱 {cfg['id']} UNEP-attributed Evidence — {cfg['short_name']}"),
                dbc.Row([
                    dbc.Col([
                        html.Label(f"Select {cfg['id']} UNEP-attributed period"),
                        dcc.Dropdown(id=f"{prefix}-unep-period", options=opts, value=default, clearable=False),
                    ], md=4),
                ], className="mb-3"),
                html.Div(id=f"{prefix}-unep-content"),
            ])
            return sp71_warning_wrapper(section_content) if is_sp71 else section_content

        if section == "report":
            period_opts = [{"label": x, "value": x} for x in p["periods"]]
            entity_opts = [{"label": x, "value": x} for x in p["entities"]]
            section_content = html.Div([
                html.H4(f"📄 {cfg['id']} Country-Period Report — {cfg['short_name']}"),
                dbc.Row([
                    dbc.Col([
                        html.Label(f"Select {cfg['id']} report period"),
                        dcc.Dropdown(id=f"{prefix}-report-period", options=period_opts,
                                     value=p["periods"][0] if p["periods"] else None, clearable=False),
                    ], md=6),
                    dbc.Col([
                        html.Label(f"Select {cfg['id']} report country/entity"),
                        dcc.Dropdown(id=f"{prefix}-report-country", options=entity_opts,
                                     value=p["entities"][0] if p["entities"] else None, clearable=False),
                    ], md=6),
                ], className="mb-3"),
                html.Div(id=f"{prefix}-report-output"),
                html.Div(id=f"{prefix}-report-download-text", style={"display": "none"}),
                dbc.Button(f"Download {cfg['id']} country-period evidence highlights report",
                           id=f"{prefix}-download-report-btn", color="secondary", className="mt-3"),
                dcc.Download(id=f"{prefix}-download-report"),
            ])
            return sp71_warning_wrapper(section_content) if is_sp71 else section_content

        if section == "explorer":
            evidence_countries = p["entities"]
            evidence_periods = p["periods"]
            section_content = html.Div([
                html.H4(f"🔎 {cfg['id']} Evidence Explorer — {cfg['short_name']}"),
                dbc.Row([
                    dbc.Col([
                        html.Label(f"Choose {cfg['id']} evidence dataset"),
                        dcc.RadioItems(
                            id=f"{prefix}-explorer-dataset",
                            options=[
                                {"label": "General evidence", "value": "General evidence"},
                                {"label": "UNEP-attributed evidence", "value": "UNEP-attributed evidence"},
                            ],
                            value="General evidence",
                            inline=True,
                        ),
                    ], md=3),
                    dbc.Col([
                        html.Label(f"{cfg['id']} evidence country/entity"),
                        dcc.Dropdown(id=f"{prefix}-explorer-country",
                                     options=[{"label": x, "value": x} for x in evidence_countries],
                                     value=evidence_countries[0] if evidence_countries else None, clearable=False),
                    ], md=3),
                    dbc.Col([
                        html.Label(f"{cfg['id']} evidence period"),
                        dcc.Dropdown(id=f"{prefix}-explorer-period",
                                     options=[{"label": x, "value": x} for x in evidence_periods],
                                     value=evidence_periods[0] if evidence_periods else None, clearable=False),
                    ], md=3),
                    dbc.Col([
                        html.Label("Keyword search"),
                        dcc.Input(id=f"{prefix}-explorer-keyword", value="", type="text", debounce=True,
                                  className="form-control"),
                    ], md=3),
                ], className="mb-3"),
                html.Div(id=f"{prefix}-explorer-output"),
                dbc.Button(f"Download filtered {cfg['id']} evidence CSV", id=f"{prefix}-download-csv-btn",
                           color="secondary", className="mt-3"),
                dcc.Download(id=f"{prefix}-download-csv"),
            ])
            return sp71_warning_wrapper(section_content) if is_sp71 else section_content

        return dbc.Alert("Unknown section.", color="warning")

    @app.callback(
        Output(f"{prefix}-general-content", "children"),
        Input(f"{prefix}-general-period", "value"),
        prevent_initial_call=False,
    )
    def update_general(period):
        p = PREPARED[cfg["id"]]
        gp = p["general_period"]
        if gp.empty or not period:
            return dbc.Alert("No general country/institution evidence summary could be built from the available files.",
                             color="warning")
        dfp = gp[gp["TimeWindow"].astype(str).str.strip() == str(period).strip()].copy()
        if dfp.empty:
            return dbc.Alert(f"No general evidence data for {period}.", color="warning")
        if "general_score" not in dfp.columns:
            dfp["general_score"] = 0
        display_cols = unique_cols([c for c in [
            "Entity", "TimeWindow", "general_score", "max_general_score",
            "count_general_evidence_docs", "best_evidence_title",
            "best_evidence_link", "best_evidence_type", "best_evidence_action_stage",
            "best_evidence_level", "best_evidence_justification", "best_evidence_phrases",
        ] if c in dfp.columns])
        table_df = dfp[display_cols].sort_values("general_score",
                                                 ascending=False) if "general_score" in dfp.columns else dfp[
            display_cols]
        return html.Div([
            dcc.Graph(figure=score_map_fig(dfp, "general_score", f"{cfg['id']} general evidence score — {period}",
                                           "Viridis")),
            html.H5("Country/institution evidence table"),
            data_table(table_df, page_size=15),
        ])

    @app.callback(
        Output(f"{prefix}-unep-content", "children"),
        Input(f"{prefix}-unep-period", "value"),
        prevent_initial_call=False,
    )
    def update_unep(period):
        p = PREPARED[cfg["id"]]
        dfu_all = p["period"]
        if dfu_all.empty or not period:
            return dbc.Alert("No UNEP-attributed country-period summary available.", color="warning")
        dfu = dfu_all[dfu_all["TimeWindow"].astype(str).str.strip() == str(period).strip()].copy()
        if dfu.empty:
            return dbc.Alert(f"No UNEP-attributed data for {period}.", color="warning")
        display_cols = unique_cols([c for c in [
            "Entity", "TimeWindow", "unep_score_for_app", "unep_extent_for_app",
            "count_attributable_docs_nonzero_unep", "best_evidence_title",
            "best_evidence_link", "best_evidence_type", "best_evidence_action_stage",
            "best_evidence_level", "best_evidence_phrases", "best_evidence_unep_justification",
        ] if c in dfu.columns])
        table_df = dfu[display_cols].sort_values("unep_score_for_app",
                                                 ascending=False) if "unep_score_for_app" in dfu.columns else dfu[
            display_cols]
        return html.Div([
            dcc.Graph(figure=score_map_fig(dfu, "unep_score_for_app",
                                           f"{cfg['id']} UNEP-attributed evidence score — {period}", "YlGn")),
            html.H5("UNEP-attributed evidence table"),
            data_table(table_df, page_size=15),
        ])

    @app.callback(
        Output(f"{prefix}-report-output", "children"),
        Output(f"{prefix}-report-download-text", "children"),
        Input(f"{prefix}-report-period", "value"),
        Input(f"{prefix}-report-country", "value"),
        prevent_initial_call=False,
    )
    def update_report(period, country):
        p = PREPARED[cfg["id"]]
        gp = p["general_period"]
        up = p["period"]

        if not period or not country:
            return dbc.Alert("Select a country/entity and period.", color="warning"), ""

        general_data = pd.DataFrame()
        if not gp.empty and {"Entity", "TimeWindow"}.issubset(gp.columns):
            general_data = gp[
                (gp["Entity"].astype(str).str.strip() == str(country).strip())
                & (gp["TimeWindow"].astype(str).str.strip() == str(period).strip())
                ].copy()

        unep_data = pd.DataFrame()
        if not up.empty and {"Entity", "TimeWindow"}.issubset(up.columns):
            unep_data = up[
                (up["Entity"].astype(str).str.strip() == str(country).strip())
                & (up["TimeWindow"].astype(str).str.strip() == str(period).strip())
                ].copy()

        general_docs = filter_general_docs(cfg, p["country_docs_for_general"], country, period)
        unep_docs = filter_unep_docs(cfg, p["docs"], country, period)

        general_score = safe_get(general_data.iloc[0], "general_score", 0) if not general_data.empty else 0
        unep_score = safe_get(unep_data.iloc[0], "unep_score_for_app", 0) if not unep_data.empty else 0

        general_card_children = [html.H5(f"General {cfg['short_name']} evidence")]
        if general_data.empty:
            general_card_children.append(
                dbc.Alert("No general indicator evidence found for this country-period.", color="light"))
        else:
            r = general_data.iloc[0]
            general_card_children.extend([
                html.H3(str(safe_get(r, "general_score", 0))),
                html.P([html.B("Evidence documents: "), str(safe_get(r, "count_general_evidence_docs", 0))]),
                html.P([html.B("Best evidence title: "), str(safe_get(r, "best_evidence_title", "N/A"))]),
                html.A("Open best evidence link", href=str(safe_get(r, "best_evidence_link", "")),
                       target="_blank") if safe_get(r, "best_evidence_link", "") else html.Span(),
                html.Details([
                    html.Summary("Evidence justification"),
                    html.Div(str(safe_get(r, "best_evidence_justification", "No justification available.")))
                ]),
                html.Details([
                    html.Summary("Evidence phrases"),
                    html.Ul([html.Li(str(x)) for x in
                             parse_evidence_phrases(safe_get(r, "best_evidence_phrases", "[]"))]) or html.Div(
                        "No evidence phrases available.")
                ]),
            ])

        unep_card_children = [html.H5(f"UNEP-attributed {cfg['short_name']} evidence")]
        if unep_data.empty:
            unep_card_children.append(
                dbc.Alert("No UNEP-attributed evidence found for this country-period.", color="light"))
        else:
            r = unep_data.iloc[0]
            unep_card_children.extend([
                html.H3(str(safe_get(r, "unep_score_for_app", 0))),
                html.P([html.B("Evidence level: "), str(safe_get(r, "unep_extent_for_app", "N/A"))]),
                html.P([html.B("Attributable evidence documents: "),
                        str(safe_get(r, "count_attributable_docs_nonzero_unep", 0))]),
                html.P([html.B("Best evidence title: "), str(safe_get(r, "best_evidence_title", "N/A"))]),
                html.A("Open best evidence link", href=str(safe_get(r, "best_evidence_link", "")),
                       target="_blank") if safe_get(r, "best_evidence_link", "") else html.Span(),
                html.Details([
                    html.Summary("UNEP attribution justification"),
                    html.Div(str(safe_get(r, "best_evidence_unep_justification",
                                          "No UNEP attribution justification available.")))
                ]),
                html.Details([
                    html.Summary("Evidence phrases"),
                    html.Ul([html.Li(str(x)) for x in
                             parse_evidence_phrases(safe_get(r, "best_evidence_phrases", "[]"))]) or html.Div(
                        "No evidence phrases available.")
                ]),
            ])

        report_lines = []
        report_lines.append(f"# {cfg['id']} Evidence Highlights Report")
        report_lines.append(f"Subprogramme: {cfg['subprogramme']}")
        report_lines.append(f"Indicator: {cfg['full_name']}")
        report_lines.append(f"Country/entity: {country}")
        report_lines.append(f"Period: {period}")
        report_lines.append("")
        report_lines.append("## General evidence")
        if general_docs.empty:
            report_lines.append("No relevant general evidence documents found.")
        else:
            contribution_col, general_col, unep_col = get_doc_score_cols(cfg, general_docs)
            justification_col = first_existing_col(general_docs, cfg["justification_candidates"])
            for _, row in general_docs.iterrows():
                report_lines.append(f"### {safe_get(row, 'Title', 'Untitled document')}")
                report_lines.append(f"Score: {safe_get(row, general_col, 'N/A')}")
                report_lines.append(f"Link: {safe_get(row, 'Link', '')}")
                report_lines.append(f"Justification: {safe_get(row, justification_col, '')}")
                report_lines.append("Evidence phrases:")
                phrases = parse_evidence_phrases(safe_get(row, "evidence_phrases", "[]"))
                if phrases:
                    for phrase in phrases:
                        report_lines.append(f"- {phrase}")
                else:
                    report_lines.append("- No evidence phrases available.")
                report_lines.append("")

        report_lines.append("")
        report_lines.append("## UNEP-attributed evidence")
        if unep_docs.empty:
            report_lines.append("No relevant UNEP-attributed evidence documents found.")
        else:
            contribution_col, general_col, unep_col = get_doc_score_cols(cfg, unep_docs)
            justification_col = first_existing_col(unep_docs, cfg["justification_candidates"])
            for _, row in unep_docs.iterrows():
                report_lines.append(f"### {safe_get(row, 'Title', 'Untitled document')}")
                report_lines.append(f"Contribution score: {safe_get(row, contribution_col, 'N/A')}")
                report_lines.append(f"Evidence score: {safe_get(row, general_col, 'N/A')}")
                report_lines.append(f"UNEP attribution score: {safe_get(row, unep_col, 'N/A')}")
                report_lines.append(f"Link: {safe_get(row, 'Link', '')}")
                report_lines.append(f"Evidence justification: {safe_get(row, justification_col, '')}")
                report_lines.append(f"UNEP justification: {safe_get(row, 'unep_justification', '')}")
                report_lines.append("Evidence phrases:")
                phrases = parse_evidence_phrases(safe_get(row, "evidence_phrases", "[]"))
                if phrases:
                    for phrase in phrases:
                        report_lines.append(f"- {phrase}")
                else:
                    report_lines.append("- No evidence phrases available.")
                report_lines.append("")

        report_text = prepare_download_text(report_lines)

        general_cols = unique_cols([c for c in [
            "Entity", "TimeWindow", "Title", "Link",
            first_existing_col(general_docs, cfg["general_score_candidates"]) if not general_docs.empty else None,
            "sd", "unep_attribution_score", "attributable_relevant_doc",
            "instrument_type", "action_stage", "evidence_level",
            *cfg["justification_candidates"], "unep_justification", "evidence_phrases",
        ] if c and not general_docs.empty and c in general_docs.columns])

        unep_cols = unique_cols([c for c in [
            "Entity", "TimeWindow", "Title", "Link", "sd",
            first_existing_col(unep_docs, cfg["general_score_candidates"]) if not unep_docs.empty else None,
            "unep_attribution_score", "attributable_relevant_doc",
            "instrument_type", "action_stage", "evidence_level",
            *cfg["justification_candidates"], "unep_justification", "evidence_phrases",
        ] if c and not unep_docs.empty and c in unep_docs.columns])

        content = html.Div([
            html.Div(f"Current filters applied: {country} | {period}", className="text-muted mb-2"),
            html.H4(f"{country} — {period}"),
            dbc.Row([
                dbc.Col(dbc.Card(dbc.CardBody(general_card_children), className="h-100"), md=6),
                dbc.Col(dbc.Card(dbc.CardBody(unep_card_children), className="h-100"), md=6),
            ], className="g-3"),
            html.Hr(),
            html.H4("Executive interpretation"),
            html.P(
                f"For {country} during {period}, the dashboard identifies a general evidence score of {general_score} "
                f"and a UNEP-attributed evidence score of {unep_score} for {cfg['id']} — {cfg['short_name']}. "
                f"These scores are based on evidence found in harvested documents and should be reviewed alongside "
                f"the source links, evidence phrases and justifications below."
            ),
            html.Hr(),
            html.H3("📚 Detailed Evidence Highlights"),
            html.H4("1. General evidence documents"),
            data_table(general_docs[general_cols] if general_cols else pd.DataFrame(), page_size=10),
            html.H4("2. UNEP-attributed evidence documents"),
            data_table(unep_docs[unep_cols] if unep_cols else pd.DataFrame(), page_size=10),
        ])

        return content, report_text

    @app.callback(
        Output(f"{prefix}-download-report", "data"),
        Input(f"{prefix}-download-report-btn", "n_clicks"),
        State(f"{prefix}-report-download-text", "children"),
        State(f"{prefix}-report-country", "value"),
        State(f"{prefix}-report-period", "value"),
        prevent_initial_call=True,
    )
    def download_report(n_clicks, text, country, period):
        if not n_clicks or not text:
            return no_update
        filename = f"{cfg['id']}_{country}_{period}_evidence_highlights.md".replace(" ", "_").replace("/", "_").replace(
            ".", "_")
        return dict(content=text, filename=filename, type="text/markdown")

    @app.callback(
        Output(f"{prefix}-explorer-output", "children"),
        Input(f"{prefix}-explorer-dataset", "value"),
        Input(f"{prefix}-explorer-country", "value"),
        Input(f"{prefix}-explorer-period", "value"),
        Input(f"{prefix}-explorer-keyword", "value"),
        prevent_initial_call=False,
    )
    def update_explorer(dataset_choice, country, period, keyword):
        p = PREPARED[cfg["id"]]
        if dataset_choice == "General evidence":
            evidence_df = p["country_docs_for_general"].copy()
            score_col = first_existing_col(evidence_df, cfg["general_score_candidates"])
        else:
            evidence_df = p["docs"].copy()
            score_col = "sd" if "sd" in evidence_df.columns else first_existing_col(evidence_df,
                                                                                    cfg["unep_score_candidates"])

        if evidence_df.empty:
            return dbc.Alert("Selected evidence dataset is empty.", color="warning")

        evidence_df = clean_timewindow(evidence_df)

        filtered = evidence_df.copy()
        if "Entity" in filtered.columns and country:
            filtered = filtered[filtered["Entity"].astype(str).str.strip() == str(country).strip()]
        if "TimeWindow" in filtered.columns and period:
            filtered = filtered[filtered["TimeWindow"].astype(str).str.strip() == str(period).strip()]

        if dataset_choice == "General evidence":
            relevant_col = first_existing_col(filtered, cfg["relevant_col_candidates"])
            if relevant_col:
                filtered = filtered[filtered[relevant_col].apply(bool_from_value)]
            general_score_col = first_existing_col(filtered, cfg["general_score_candidates"])
            if general_score_col:
                filtered[general_score_col] = pd.to_numeric(filtered[general_score_col], errors="coerce").fillna(0)
                filtered = filtered[filtered[general_score_col] > 0]
                score_col = general_score_col
        else:
            filtered = filter_unep_docs(cfg, filtered, country, period)

        if keyword:
            keyword_lower = str(keyword).lower()
            text_cols = [c for c in [
                "Title", "capacity_justification", "climate_justification",
                "nature_justification", "chemicals_justification", "pollution_justification",
                "env_law_justification", "environmental_law_justification",
                "finance_justification", "digital_justification", "unep_justification",
                "evidence_phrases",
            ] if c in filtered.columns]
            mask = pd.Series(False, index=filtered.index)
            for c in text_cols:
                mask = mask | filtered[c].astype(str).str.lower().str.contains(keyword_lower, na=False)
            filtered = filtered[mask]

        if score_col and score_col in filtered.columns:
            filtered[score_col] = pd.to_numeric(filtered[score_col], errors="coerce").fillna(0)
            filtered = filtered.sort_values(score_col, ascending=False)

        display_cols = unique_cols([c for c in [
            "Entity", "TimeWindow", "Title", "Link", score_col, "sd",
            "capacity_score", "climate_policy_score", "nature_framework_score",
            "policy_regulation_score", "chemicals_policy_score", "pollution_policy_score",
            "env_law_score", "environmental_law_score", "finance_policy_score",
            "digital_practice_score", "unep_attribution_score", "unep_attributed",
            "attributable_relevant_doc", "instrument_type", "improvement_type",
            "action_stage", "actor_type", "evidence_level", "capacity_justification",
            "climate_justification", "nature_justification", "chemicals_justification",
            "pollution_justification", "env_law_justification", "environmental_law_justification",
            "finance_justification", "digital_justification", "unep_justification",
            "evidence_phrases",
        ] if c and c in filtered.columns])

        # Store filtered data in global cache for download
        FILTERED_CACHE[f"{prefix}-explorer"] = filtered[display_cols].copy() if display_cols else pd.DataFrame()

        return html.Div([
            html.P(f"Documents found: {len(filtered)}"),
            data_table(FILTERED_CACHE[f"{prefix}-explorer"], page_size=15),
        ])

    @app.callback(
        Output(f"{prefix}-download-csv", "data"),
        Input(f"{prefix}-download-csv-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def download_csv(n_clicks):
        if not n_clicks:
            return no_update
        df = FILTERED_CACHE.get(f"{prefix}-explorer", pd.DataFrame())
        if df.empty:
            return no_update
        return dcc.send_data_frame(df.to_csv, f"{cfg['id']}_filtered_evidence.csv".replace(".", "_"), index=False,
                                   encoding="utf-8-sig")


FILTERED_CACHE = {}

for cfg in INDICATORS:
    make_indicator_callbacks(cfg)


# ============================================================
# SP4.2 CALLBACK
# ============================================================

@app.callback(
    Output("sp42-content", "children"),
    Input("sp42-tabs", "value"),
    prevent_initial_call=False,
)
def render_sp42(tab):
    if overton_42.empty:
        return dbc.Alert("No Indicator 4.2 data found.", color="warning")

    valid = overton_42[
        ~overton_42["TimeWindow_42"].astype(str).isin(["Outside dashboard periods", "Unknown", "nan", "None", ""])
    ].copy()

    if tab == "overview":
        if valid.empty:
            return dbc.Alert("No valid Indicator 4.2 records available.", color="warning")

        period_summary = valid.groupby("TimeWindow_42").agg(
            governments_or_institutions=("User_entity_42", "nunique"),
            countries_or_territories=("Entity_42", "nunique"),
            candidate_documents=("Overton id", "count"),
        ).reset_index()

        fig_docs = px.bar(
            period_summary,
            x="TimeWindow_42",
            y="candidate_documents",
            text="candidate_documents",
            title="Indicator 4.2 candidate documents by period",
        )

        return html.Div([
            dbc.Row([
                dbc.Col(metric_card("Candidate documents", len(valid)), md=4),
                dbc.Col(metric_card("Countries/territories represented", valid["Entity_42"].nunique()), md=4),
                dbc.Col(metric_card("Government/public-sector institutions", valid["User_entity_42"].nunique()), md=4),
            ], className="g-3 mb-3"),
            dcc.Graph(figure=fig_docs),
            data_table(period_summary, page_size=10),
        ])

    if tab == "map":
        if valid.empty:
            return dbc.Alert("No valid Indicator 4.2 records available.", color="warning")

        map_df = valid.groupby("Entity_42").agg(candidate_documents=("Overton id", "count")).reset_index()
        fig = px.choropleth(
            map_df,
            locations="Entity_42",
            locationmode="country names",
            color="candidate_documents",
            hover_name="Entity_42",
            color_continuous_scale="Viridis",
            title="Indicator 4.2 candidate evidence by country/territory",
        )
        fig.update_layout(geo=dict(showframe=False, showcoastlines=True), height=560, margin=dict(l=0, r=0, t=50, b=0))
        return html.Div([
            dcc.Graph(figure=fig),
            data_table(map_df.sort_values("candidate_documents", ascending=False), page_size=20),
        ])

    if tab == "report":
        periods = sorted(valid["TimeWindow_42"].dropna().astype(str).unique())
        countries = sorted(valid["Entity_42"].dropna().astype(str).unique())
        return html.Div([
            dbc.Row([
                dbc.Col([
                    html.Label("Select Indicator 4.2 period"),
                    dcc.Dropdown(id="sp42-report-period", options=[{"label": p, "value": p} for p in periods],
                                 value=periods[0] if periods else None, clearable=False),
                ], md=6),
                dbc.Col([
                    html.Label("Select Indicator 4.2 country/territory"),
                    dcc.Dropdown(id="sp42-report-country", options=[{"label": c, "value": c} for c in countries],
                                 value=countries[0] if countries else None, clearable=False),
                ], md=6),
            ], className="mb-3"),
            html.Div(id="sp42-report-output"),
        ])

    return dbc.Alert("Unknown Indicator 4.2 tab.", color="warning")


@app.callback(
    Output("sp42-report-output", "children"),
    Input("sp42-report-period", "value"),
    Input("sp42-report-country", "value"),
    prevent_initial_call=False,
)
def update_sp42_report(period, country):
    if overton_42.empty or not period or not country:
        return dbc.Alert("Select a period and country/territory.", color="warning")

    valid = overton_42[
        ~overton_42["TimeWindow_42"].astype(str).isin(["Outside dashboard periods", "Unknown", "nan", "None", ""])
    ].copy()
    df = valid[
        (valid["TimeWindow_42"].astype(str) == str(period))
        & (valid["Entity_42"].astype(str) == str(country))
        ].copy()

    if df.empty:
        return dbc.Alert(f"No Indicator 4.2 candidate evidence found for {country} — {period}.", color="light")

    display_cols = [c for c in [
        "Entity_42", "TimeWindow_42", "User_entity_42", "Title", "Document type",
        "Source title", "Source organisation type", "Source sector", "Published_on",
        "Document URL", "Overton URL", "Top topics", "Related to SDGs", "Document theme",
    ] if c in df.columns]

    return html.Div([
        html.H4(f"{country} — {period}"),
        dbc.Row([
            dbc.Col(metric_card("Candidate documents", len(df)), md=4),
            dbc.Col(metric_card("Institutions represented", df["User_entity_42"].nunique()), md=4),
            dbc.Col(metric_card("Document types",
                                df["Document type"].nunique() if "Document type" in df.columns else "N/A"), md=4),
        ], className="g-3 mb-3"),
        data_table(df[display_cols], page_size=15),
    ])


# ============================================================
# CSS
# ============================================================

app.index_string = """
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>{%title%}</title>
        {%favicon%}
        {%css%}
        <style>
            body {
                background-color: #f8fafc;
            }
            .app-header {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                padding: 18px 22px;
                margin: 16px 0;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
            }
            .app-title {
                margin: 0;
                color: #0f172a;
                font-weight: 700;
            }
            .app-subtitle {
                color: #64748b;
                margin-top: 4px;
            }
            .main-content {
                background: white;
                border: 1px solid #e5e7eb;
                border-radius: 14px;
                padding: 20px;
                margin-top: 12px;
                margin-bottom: 32px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
            }
            .metric-card {
                border: 1px solid #e5e7eb;
                border-radius: 12px;
                box-shadow: 0 1px 2px rgba(15, 23, 42, 0.06);
            }
            .metric-title {
                color: #64748b;
                font-size: 0.92rem;
                font-weight: 600;
            }
            .metric-value {
                color: #0f172a;
                font-size: 2rem;
                font-weight: 800;
                line-height: 1.2;
            }
            .metric-subtitle {
                color: #94a3b8;
                font-size: 0.85rem;
            }
            .tab {
                padding: 12px !important;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
"""

# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    app.run(debug=True, port=8050)
