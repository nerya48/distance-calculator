import streamlit as st
import googlemaps
import pandas as pd

# ----------------------------------------------------
# 1) הגדרת API Key ויצירת לקוח Google Maps
# ----------------------------------------------------
API_KEY = "AIzaSyBlo9MobgTHKPWnNh8xzLiioQItIRo5CYA"  # המפתח התקין שלך מגוגל קלאוד
gmaps = googlemaps.Client(key=API_KEY)

def get_distance(origin, destination):
    """
    מחזירה מחרוזת של מרחק, למשל '33.2 km'.
    משתמשת ב-distance_matrix של googlemaps.
    """
    res = gmaps.distance_matrix(origins=origin, destinations=destination, mode="driving")
    return res['rows'][0]['elements'][0]['distance']['text']  # 'xx.x km'

def distance_to_float(distance_text):
    """
    הופכת '33.2 km' ל-33.2 (float).
    """
    clean = distance_text.replace("km", "").strip()
    return float(clean)

# ----------------------------------------------------
# 3) כותרת לאפליקציה ועיצוב בסיסי
# ----------------------------------------------------
st.set_page_config(page_title="Distance Calculator", layout="centered")
st.image("https://raw.githubusercontent.com/nerya48/distance-calculator/main/PIC.jpg", width=200)
st.title("📍 מחשבון מרחקים - הלוך חזור")
st.markdown("### מחשב מרחק הלוך-חזור בין כתובת מקור ליעדים ומחשב עלות דלק.")

# ----------------------------------------------------
# 4) בחירת מקור
# ----------------------------------------------------
DEFAULT_ORIGIN = "Beit Shemesh Roy Klein 21"

st.sidebar.header("הגדרות מקור")
use_default = st.sidebar.radio("האם להשתמש במקור ברירת המחדל?", ["כן", "לא"], index=0)

if use_default == "כן":
    origin = DEFAULT_ORIGIN
else:
    origin = st.sidebar.text_input("הכנס כתובת מקור חלופית:", value="")

st.sidebar.markdown(f"📍 **כתובת מקור נבחרת:** {origin or '[לא הוזנה]'}")

# ----------------------------------------------------
# 5) קבלת יעדים בבת אחת
# ----------------------------------------------------
st.header("💼 הוספת יעדים")
destinations_str = st.text_area("🔹 הדבק כאן כתובות יעד (מופרדות בפסיק):", "")
destinations = [d.strip() for d in destinations_str.split(",") if d.strip()]

# ----------------------------------------------------
# 6) טבלה לעריכת נתונים
# ----------------------------------------------------
if destinations:
    st.markdown("### עריכת מקור עבור כל יעד")
    data = {
        "יעד": destinations,
        "כתובת מקור": [origin] * len(destinations),
    }
    df = pd.DataFrame(data)

    # מציג טבלה עם אפשרות לערוך
    edited_df = st.experimental_data_editor(df, use_container_width=True)

    # כפתור עדכון
    if st.button("📊 עדכן וחישוב מרחקים"):
        # ------------------------------------------------
        # 7) חישוב מרחקים
        # ------------------------------------------------
        results = []
        for index, row in edited_df.iterrows():
            origin = row["כתובת מקור"]
            destination = row["יעד"]

            try:
                going_text = get_distance(origin, destination)
                return_text = get_distance(destination, origin)
                total_num = distance_to_float(going_text) + distance_to_float(return_text)
                total_text = f"{total_num:.2f} km"
                cost_num = total_num * 0.6
                cost_text = f"{cost_num:.2f} ₪"

                # שומר תוצאות
                results.append([destination, total_text, cost_text])

            except Exception as e:
                st.error(f"שגיאה בחישוב המרחק עבור {destination}: {e}")

        # ------------------------------------------------
        # 8) הצגת תוצאות
        # ------------------------------------------------
        if results:
            st.subheader("🔍 תוצאות חישוב")
            df_results = pd.DataFrame(results, columns=["יעד", "מרחק הלוך-חזור (ק\"מ)", "עלות (ש\"ח)"])
            st.dataframe(df_results, use_container_width=True)

            # --------------------------------------------
            # 9) יצוא לאקסל
            # --------------------------------------------
            st.download_button(
                label="📥 הורד קובץ Excel",
                data=df_results.to_csv(index=False).encode('utf-8'),
                file_name="distances_round_trip.csv",
                mime="text/csv"
            )
