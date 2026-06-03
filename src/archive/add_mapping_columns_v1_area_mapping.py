import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[1]

input_path = BASE_DIR / "data" / "raw" / "hwaseong_small_libraries_mapping.csv"

output_dir = BASE_DIR / "data" / "processed"
output_path = output_dir / "hwaseong_small_libraries_mapped.csv"
failed_output_path = output_dir / "mapping_failed_rows.csv"

# data/processed 폴더가 없으면 자동으로 만들기
output_dir.mkdir(parents=True, exist_ok=True)

df = pd.read_csv(input_path, encoding="utf-8-sig")

# 문자열 컬럼을 먼저 만들어두기
df["매핑_행정구역"] = pd.Series(pd.NA, index=df.index, dtype="object")
df["매핑상태"] = pd.Series("수동확인필요", index=df.index, dtype="object")
df["비고"] = pd.Series(pd.NA, index=df.index, dtype="object")

areas = [
    "우정읍", "향남읍", "남양읍", "마도면", "송산면", "서신면",
    "팔탄면", "장안면", "양감면", "새솔동", "봉담읍", "매송면",
    "비봉면", "정남면", "기배동", "진안동", "병점1동", "병점2동",
    "반월동", "화산동", "동탄1동", "동탄2동", "동탄3동", "동탄4동",
    "동탄5동", "동탄6동", "동탄7동", "동탄8동", "동탄9동"
]

for area in areas:
    mask = df["소재지"].str.contains(area, na=False, regex=False)
    df.loc[mask, "매핑_행정구역"] = area
    df.loc[mask, "매핑상태"] = "매핑완료"

# 매핑 안 된 행 찾기
not_mapped = df["매핑_행정구역"].isna()

df.loc[not_mapped, "매핑상태"] = "수동확인필요"
df.loc[not_mapped, "비고"] = "소재지에서 행정구역을 자동으로 찾지 못함"

failed_df = df[not_mapped].copy()

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

print("매핑 완료")
print("전체 저장 위치:", output_path)
print("매핑 실패 저장 위치:", failed_output_path)
print()
print(df["매핑상태"].value_counts())
print()
print(df[["도서관명", "소재지", "매핑_행정구역", "매핑상태", "비고"]].head(20))