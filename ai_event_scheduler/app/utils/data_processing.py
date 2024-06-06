import matplotlib
matplotlib.use('Agg')  # Use the non-GUI backend for matplotlib
import matplotlib.pyplot as plt


def generate_engagement_report():
    import pandas as pd
    from io import BytesIO
    import base64
    import matplotlib.pyplot as plt  # Ensure this is imported here if matplotlib.use('Agg') is set at the top of the file

    # Example data
    data = {
        "dates": ["2021-01-01", "2021-02-01", "2021-03-01"],
        "user_engagement": [120, 150, 130]
    }
    df = pd.DataFrame(data)
    df['dates'] = pd.to_datetime(df['dates'])
    
    # Plotting
    plt.figure(figsize=(10, 5))
    plt.plot(df['dates'], df['user_engagement'], marker='o')
    plt.title('Monthly User Engagement')
    plt.xlabel('Date')
    plt.ylabel('Engagement Level')
    plt.grid(True)
    plt.tight_layout()

    # Save plot to a bytes buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    
    # Encode PNG image to base64 string
    image_png = buffer.getvalue()
    graph = base64.b64encode(image_png)
    graph = graph.decode('utf-8')
    buffer.close()
    
    return graph
