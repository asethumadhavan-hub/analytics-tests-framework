def transform_customer_dim(df):
    df = df.copy()
    df["full_name"] = df["first_name"].str.strip() + " " + df["last_name"].str.strip()
    df["is_active"] = df["status"].str.lower().eq("active")
    return df[["customer_id", "full_name", "is_active"]]
