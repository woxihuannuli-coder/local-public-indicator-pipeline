import pytest

ALLOWED_REGION_GU = {"동탄구", "만세구", "효행구", "병점구"}


def test_region_gu_not_null(small_libraries_df):
    assert small_libraries_df["region_gu"].notna().all()


def test_region_gu_allowed_values(small_libraries_df):
    actual_values = set(small_libraries_df["region_gu"].dropna().unique())
    assert actual_values <= ALLOWED_REGION_GU

def test_region_gu_not_null_detect_error(small_libraries_df):
    broken_df = small_libraries_df.copy()
    broken_df.loc[0, "region_gu"] = None
    with pytest.raises(AssertionError):
        assert broken_df["region_gu"].notna().all()

def test_invalid_region_gu_value(small_libraries_df):
    broken_df = small_libraries_df.copy()
    broken_df.loc[0,"region_gu"] = "팔달구"
    with pytest.raises(AssertionError):
        actual_values = set(broken_df["region_gu"].dropna().unique())
        assert actual_values <= ALLOWED_REGION_GU

def test_mapping_status_not_null(small_libraries_df):
    assert small_libraries_df["매핑상태"].notna().all()


def test_mapping_status_not_null_detect_error(small_libraries_df):
    broken_df = small_libraries_df.copy()
    broken_df.loc[0, "매핑상태"] = None

    with pytest.raises(AssertionError):
        assert broken_df["매핑상태"].notna().all()


def test_duplicate_library_not_exists(small_libraries_df):
    duplicated_count = small_libraries_df.duplicated(
        subset=["도서관명", "소재지"]
    ).sum()

    assert duplicated_count == 0


def test_duplicate_library_detect_error(small_libraries_df):
    broken_df = small_libraries_df.copy()
    broken_df.loc[len(broken_df)] = broken_df.loc[0]

    with pytest.raises(AssertionError):
        duplicated_count = broken_df.duplicated(
            subset=["도서관명", "소재지"]
        ).sum()

        assert duplicated_count == 0


