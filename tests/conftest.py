from pathlib import Path

import pandas as pd
import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DATA_PATH = (
    PROJECT_ROOT
    / "data"
    / "processed"
    / "hwaseong_small_libraries_gu_mapped.csv"
)


@pytest.fixture
def small_libraries_df():
    assert DATA_PATH.exists(), f"CSV 파일을 찾을 수 없습니다: {DATA_PATH}"
    return pd.read_csv(DATA_PATH, encoding="utf-8-sig")