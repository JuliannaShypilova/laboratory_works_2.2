import urllib.request
import urllib.parse
import re
import pandas as pd
import os


def get_schedule_link(base_url):
    try:
        req = urllib.request.Request(base_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            html = response.read().decode('utf-8')
        links = re.findall(r'href="([^"]+\.xlsx?)"', html)
        return urllib.parse.urljoin(base_url, links[0]) if links else None
    except:
        return None


def normalize(s):
    return re.sub(r'[^a-zа-яіїєґ0-9]', '', str(s).lower())


def clean_lesson_content(text, target_group):
    if pd.isna(text) or not str(text).strip(): return ""

    t_low = target_group.lower()
    parts = re.split(r'\n| {3,}|;|Далі:', str(text))
    valid_parts = []

    for p in parts:
        p_strip = p.strip()
        if len(p_strip) < 3: continue
        p_low = p_strip.lower()
        group_match = re.search(r'(\d)\s*груп', p_low)
        target_group_num = re.search(r'(\d)', t_low)

        if group_match and target_group_num:
            if group_match.group(1) != target_group_num.group(1):
                continue

        others = ["середня освіта", "механіка", "статистика", "інноваційна"]
        others = [o for o in others if o not in t_low]

        has_other = any(o in p_low for o in others)
        is_general = any(k in p_low for k in ["лек", "загальн", "військ", "потік"])

        if has_other and not (t_low in p_low or is_general):
            continue

        valid_parts.append(p_strip)

    return " | ".join(valid_parts)


def show_split_schedule():
    url = "http://www.mechmat.knu.ua/golovna/fakul-tet/raspisanie/"
    link = get_schedule_link(url)
    if not link: return

    urllib.request.urlretrieve(link, "sch.xlsx")

    course = input("Курс: ")
    group = input("Спеціальність та група (напр. математика 1): ")
    day_target = input("День: ").lower()

    try:
        xl = pd.ExcelFile("sch.xlsx")
        sheet = next((s for s in xl.sheet_names if str(course) in s), xl.sheet_names[0])
        df = xl.parse(sheet, header=None)
        xl.close()

        target_col = -1
        group_norm = normalize(group)

        for c in range(df.shape[1]):
            head_area = df.iloc[:25, c].dropna().astype(str)
            head_text = normalize(" ".join(head_area))
            if group_norm in head_text:
                target_col = c
                break

        if target_col == -1:
            base_name = normalize(re.sub(r'\d', '', group))
            for c in range(df.shape[1]):
                head_area = df.iloc[:25, c].dropna().astype(str)
                head_text = normalize(" ".join(head_area))
                if base_name in head_text:
                    target_col = c
                    break

        if target_col == -1:
            print("Групу не знайдено.")
            return

        # Межі дня
        weekdays = ['понеділок', 'вівторок', 'середа', 'четвер', "п'ятниця", 'субота']
        start_row = -1
        end_row = df.shape[0]

        for i in range(df.shape[0]):
            if normalize(day_target) in normalize(df.iloc[i, 0]):
                start_row = i
                for j in range(i + 1, df.shape[0]):
                    if any(normalize(wd) in normalize(df.iloc[j, 0]) for wd in weekdays):
                        end_row = j
                        break
                break

        if start_row == -1:
            print("День не знайдено.")
            return

        print(f"\n--- РОЗКЛАД: {group.upper()} ({day_target.upper()}) ---")

        day_df = df.iloc[start_row:end_row].copy()
        day_df_filled = day_df.ffill(axis=1)

        for i in range(len(day_df)):
            raw_content = day_df_filled.iloc[i, target_col]
            if pd.notna(raw_content) and len(str(raw_content)) > 3:
                cleaned = clean_lesson_content(raw_content, group)
                if cleaned:
                    p_time = str(day_df.iloc[i, 1]).strip()
                    time_box = p_time if len(p_time) > 4 else str(day_df.iloc[i, 0]).strip()
                    print(f"{str(time_box).ljust(10)} | {cleaned}")

    except Exception as e:
        print(f"Помилка: {e}")
    finally:
        if os.path.exists("sch.xlsx"): os.remove("sch.xlsx")


if __name__ == "__main__":
    show_split_schedule()