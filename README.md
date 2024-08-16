# YouTube Metrics Analysis Project

<div align="center">
  <!-- Center the top image -->
  <img width="685" alt="tableau-dashboard" src="https://github.com/user-attachments/assets/00d0fbb1-f1a7-40de-a0cb-801465045c3f">
</div>

<br>

<div align="center">
  <!-- Display the two images side by side -->
  <img src="https://github.com/user-attachments/assets/ffa57701-17b0-48d4-a6aa-e4368110e666" alt="images-2" style="display:inline-block; margin-right: 10px; width:45%;">
  <img src="https://github.com/user-attachments/assets/060f91ac-340f-4442-adcc-312b0f5734c0" alt="images" style="display:inline-block; width:45%;">
</div>

This project provides a comprehensive analysis of YouTube metrics for BuzzFeed’s channels, focusing on extracting, analyzing, and visualizing key performance indicators. The goal is to understand both the popularity and engagement of YouTube content by defining and exploring North Star metrics and their relationships.

## Project Components

1. **Python Code**:
   - Retrieves and processes YouTube video data using the YouTube Data API v3. Extracts metrics and saves them into an Excel file.
   - **File:** `yt-analysis.py`

2. **Excel Raw Data File**:
   - Contains raw metrics data extracted from YouTube. Includes details like video ID, channel ID, title, tags, description, and various engagement metrics.
   - **File:** `buzzfeed_youtube_metrics.xlsx`

3. **Tableau Dashboard**:
   - Provides visual insights into YouTube metrics. Includes interactive charts and graphs to explore the relationship between metrics.
   - **Tableau Dashboard Link:** [BuzzFeed YouTube Metrics Dashboard](https://github.com/user-attachments/files/16631566/YT-Analysis.pdf)

## Analysis Overview

### Defining North Star Metrics

North Star metrics are critical indicators of a channel’s success and are used to gauge overall performance. For this project, we define the following North Star metrics:

- **View Count**: Measures the total number of times a video has been viewed. Indicates popularity and reach.
- **Engagement Rate**: A composite metric calculated as the sum of likes, comments, and shares relative to the view count. Reflects how actively viewers interact with the content.
- **Watch Time**: Total time spent watching the video. Provides insights into how engaging and relevant the content is.

### Defining Dimensions

Dimensions are characteristics or attributes of the data that provide context to the metrics:

- **Time**: Date published and time of day.
- **Video Characteristics**: Title, description, tags, and category.
- **Audience Interaction**: Likes, comments, shares.

### Data Calculation and Visualization

1. **Calculate Metrics**:
   - **Engagement Rate**: 
     ```excel
     = (Likes + Comments + Shares) / View Count
     ```
   - **Watch Time**: Directly obtained from the YouTube API.

2. **Visualization**:
   - **View Count vs. Engagement Rate**: Scatter plot to examine if higher views correlate with higher engagement.
   - **Likes and Comments Distribution**: Histograms to visualize the distribution of likes and comments.
   - **Watch Time by Category**: Bar chart to show average watch time across different video categories.

3. **Uncover Drivers and Relationships**:
   - **Correlation Analysis**: Use scatter plots and correlation coefficients to identify relationships between metrics like view count and engagement rate.
   - **Trend Analysis**: Analyze trends over time to understand how metrics change.

### Tableau Dashboards

1. **Channel Summary**:
   - **Metrics Displayed**: Total views, total likes, and videos uploaded for each channel.
   - **Purpose**: Provides an overview of channel performance, highlighting which channels have the most content and engagement.

2. **Performance of Shorts vs. Regular Videos**:
   - **Metrics Analyzed**: Views, likes, and comments for shorts versus regular videos.
   - **Purpose**: Compares the performance of short-form content against long-form videos, revealing trends in audience preference and engagement.

3. **Correlation Between Views and Length of Regular Videos**:
   - **Metrics Analyzed**: View count and video length in minutes for regular videos.
   - **Purpose**: Examines if there is a relationship between video length and its popularity, helping to understand the impact of video duration on views.

4. **Take Immediate Action**:
   - **Videos with No Tags**: Identifies videos that are missing tags, which may affect discoverability and performance.
   - **Least Performing Videos**: Lists videos with the lowest metrics in terms of views, likes, and comments, highlighting areas for potential improvement.

### Recommendations

- **Content Strategy**: Focus on creating content that drives high engagement rates. Videos with higher engagement metrics (likes, comments, shares) indicate stronger audience interaction.
- **Optimize Thumbnails and Titles**: Improve click-through rates by optimizing video thumbnails and titles based on analysis of high-performing videos.
- **Audience Feedback**: Leverage comments and engagement metrics to gather feedback and refine content strategies.
- **Actionable Improvements**: Address issues identified in the "Take Immediate Action" tab by adding tags to videos and enhancing the quality of underperforming content.

### Insight Summary

The analysis of BuzzFeed's YouTube channels provided several key insights:

- **Video Tagging**: There is **one video** without any tags, which could negatively impact its discoverability and performance.
- **Underperforming Videos**: **Three videos** have fewer than **50K views**, while the average view count for other videos ranges between **2-5 million**. These underperforming videos may need strategic adjustments or improvements.
- **Shorts vs. Regular Videos**: **Regular videos** receive **more than twice** the views compared to shorts, with views for regular videos being **2x** that of shorts. Despite this, shorts generate higher engagement, with likes and comments being **more prevalent** compared to regular videos.
- **Engagement Comparison**: Shorts have approximately **three times more** engagement relative to regular videos, though regular videos receive about **ten times more comments**. This indicates that while shorts drive more engagement per view, regular videos foster a higher volume of interaction.

## Instructions

1. **Set Up the Environment**:
   - Install required libraries:
     ```bash
     pip install google-api-python-client pandas python-dotenv openpyxl
     ```

2. **Configure API Key**:
   - Store your YouTube Data API key in a `.env` file:
     ```
     API_KEY=your_youtube_api_key
     ```

3. **Configure Channel IDs**:
   - Update `yt-analysis.py` with BuzzFeed’s YouTube channel IDs.

4. **Run the Script**:
   - Execute the Python script:
     ```bash
     python yt-analysis.py
     ```

5. **Review the Excel File**:
   - Open `buzzfeed_youtube_metrics.xlsx` to review the metrics.

6. **Visualize Data**:
   - Use the Tableau dashboard link to explore visualizations and insights.

## Contributing

Contributions are welcome! Feel free to submit issues, suggestions, or pull requests :)
