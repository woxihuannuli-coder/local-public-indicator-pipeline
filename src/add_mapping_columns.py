import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

input_path = BASE_DIR / "data" / "raw" / "hwaseong_small_libraries_mapping.csv"

output_dir = BASE_DIR / "data" / "processed"
output_path = output_dir / "hwaseong_small_libraries_mapped.csv"
failed_output_path = output_dir / "mapping_failed_rows.csv"

output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_path, encoding="utf-8-sig")

# 1. 새 컬럼 미리 만들기
df["region_gu"] = pd.Series(pd.NA, index=df.index, dtype="object")
df["region_detail"] = pd.Series(pd.NA, index=df.index, dtype="object")
df["join_key"] = pd.Series(pd.NA, index=df.index, dtype="object")
df["매핑상태"] = pd.Series("수동확인필요", index=df.index, dtype="object")
df["비고"] = pd.Series(pd.NA, index=df.index, dtype="object")

# 2. 구 기준 매핑
gu_list = ["동탄구", "병점구", "효행구", "만세구"]

for gu in gu_list:
    mask = df["소재지"].str.contains(gu, na=False, regex=False)
    df.loc[mask, "region_gu"] = gu
    df.loc[mask, "join_key"] = gu
    df.loc[mask, "매핑상태"] = "구기준매핑완료"

# 3. 세부 지역은 참고용으로 따로 저장
detail_list = [
    "봉담읍", "향남읍", "우정읍", "남양읍",
    "마도면", "송산면", "서신면", "팔탄면", "장안면", "양감면",
    "기안동", "영천동", "청계동", "능동", "오산동", "병점동"
]

for detail in detail_list:
    mask = df["소재지"].str.contains(detail, na=False, regex=False)
    df.loc[mask, "region_detail"] = detail

# 4. join_key가 없는 행 찾기
not_mapped = df["join_key"].isna()

df.loc[not_mapped, "매핑상태"] = "수동확인필요"
df.loc[not_mapped, "비고"] = "구 기준 join_key를 자동으로 찾지 못함"

failed_df = df[not_mapped].copy()

# 5. 결과 저장
failed_df.to_csv(
    failed_output_path,
    index=False,
    encoding="utf-8-sig"
)

df.to_csv(
    output_path,
    index=False,
    encoding="utf-8-sig"
)

# 6. 결과 확인
print("매핑 완료")
print("전체 저장 위치:", output_path)
print("매핑 실패 저장 위치:", failed_output_path)
print()
print(df["매핑상태"].value_counts())
print()
print(df[["도서관명", "소재지", "region_gu", "region_detail", "join_key", "매핑상태", "비고"]].head(30))