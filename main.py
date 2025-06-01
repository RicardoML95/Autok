from uploaders.upload_youtube import upload_youtube_video
# from uploaders.upload_instagram import upload_instagram_reel


print("🚀 Subiendo nuevo video")
upload_youtube_video(r"output\Youtube\en\flags_en_1_20250531_115354.mp4", "Guess test!", "You have 5 seconds… AutoGuessIt! #Shorts", ["shorts", "python"])
# upload_instagram_reel("videos_to_upload/video1.mp4", "¡Nuevo video!")
print("✅ Video subido a YouTube")

