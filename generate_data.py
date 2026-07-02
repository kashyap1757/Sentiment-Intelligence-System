"""Generate diverse MOVIE REVIEW prediction data for dashboard demonstration."""
import os
import random
import pandas as pd
from datetime import datetime, timedelta

reviews_data = [
    # Positive movie reviews
    ("This film was an absolute masterpiece from start to finish!", "Positive", 0.95),
    ("Brilliant performances by the entire cast, truly unforgettable.", "Positive", 0.92),
    ("The plot twists kept me on the edge of my seat throughout.", "Positive", 0.89),
    ("One of the best movies I have ever seen, a must watch!", "Positive", 0.96),
    ("The cinematography was breathtaking and visually stunning.", "Positive", 0.91),
    ("Incredible directing with a powerful emotional storyline.", "Positive", 0.93),
    ("The soundtrack perfectly complemented every scene beautifully.", "Positive", 0.87),
    ("A heartwarming story with brilliant character development.", "Positive", 0.90),
    ("Loved every minute of it, the acting was phenomenal!", "Positive", 0.94),
    ("The special effects were out of this world, jaw dropping!", "Positive", 0.88),
    ("This documentary was eye-opening and beautifully produced.", "Positive", 0.85),
    ("The sequel was even better than the original, loved it!", "Positive", 0.92),
    ("An emotional rollercoaster that left me in tears, amazing film.", "Positive", 0.93),
    ("The script was witty and the dialogue felt natural and engaging.", "Positive", 0.86),
    ("A perfect blend of action and drama, keeps you hooked.", "Positive", 0.90),
    ("The director did an outstanding job bringing this story to life.", "Positive", 0.91),
    ("This movie deserves every award it has been nominated for.", "Positive", 0.95),
    ("Beautiful storytelling with a profound and meaningful message.", "Positive", 0.89),
    ("The chemistry between the lead actors was absolutely electric.", "Positive", 0.87),
    ("A gripping thriller that never lets up from the opening scene.", "Positive", 0.92),
    ("Visually spectacular with a deeply moving narrative arc.", "Positive", 0.88),
    ("The child actors in this film were surprisingly impressive.", "Positive", 0.84),
    ("A refreshing take on the genre, original and captivating.", "Positive", 0.86),
    ("The climax was intense and perfectly executed, bravo!", "Positive", 0.91),
    ("A feel-good movie that restores your faith in cinema.", "Positive", 0.85),
    ("The world-building in this sci-fi epic was extraordinary.", "Positive", 0.93),
    ("Excellent adaptation of the novel, stayed true to the source.", "Positive", 0.88),
    ("The humor was spot on without ever feeling forced or cheap.", "Positive", 0.83),
    ("A cinematic experience that stays with you long after credits.", "Positive", 0.90),
    ("The ensemble cast delivered flawless performances throughout.", "Positive", 0.94),
    # Negative movie reviews
    ("This movie was painfully boring and completely predictable.", "Negative", 0.08),
    ("Terrible acting and a nonsensical plot from beginning to end.", "Negative", 0.05),
    ("A complete waste of two hours, the worst film this year.", "Negative", 0.03),
    ("Bad direction, poor script, and unconvincing performances.", "Negative", 0.10),
    ("Extremely disappointing sequel that ruined the franchise.", "Negative", 0.06),
    ("The plot had so many holes it became unwatchable.", "Negative", 0.11),
    ("Overrated and overhyped, did not live up to the trailer.", "Negative", 0.14),
    ("The pacing was awful, scenes dragged on for too long.", "Negative", 0.09),
    ("The CGI looked cheap and took me out of every scene.", "Negative", 0.07),
    ("None of the characters were likeable or well developed.", "Negative", 0.12),
    ("The dialogue was cringeworthy and felt extremely forced.", "Negative", 0.08),
    ("A lazy cash grab with zero creativity or originality.", "Negative", 0.04),
    ("The ending ruined what could have been a decent film.", "Negative", 0.13),
    ("Boring storyline with zero tension or emotional depth.", "Negative", 0.09),
    ("The audio mixing was terrible, could barely hear the dialogue.", "Negative", 0.11),
    ("Fell asleep halfway through, says everything about this movie.", "Negative", 0.06),
    ("The villain was laughably bad with no real motivation.", "Negative", 0.10),
    ("This remake was completely unnecessary and poorly executed.", "Negative", 0.05),
    ("Confusing timeline that made the plot impossible to follow.", "Negative", 0.08),
    ("The movie relies too heavily on shock value with no substance.", "Negative", 0.07),
    ("Poorly written characters with no depth or development at all.", "Negative", 0.09),
    ("The romantic subplot felt forced and added nothing to the story.", "Negative", 0.12),
    ("An absolute disaster from casting to final edit.", "Negative", 0.03),
    ("Too many unnecessary subplots that went absolutely nowhere.", "Negative", 0.11),
    ("The twist ending was obvious from the very first scene.", "Negative", 0.15),
    ("Wooden performances from actors I know can do much better.", "Negative", 0.10),
    ("The comedy fell flat, not a single joke landed.", "Negative", 0.08),
    ("Overly long runtime with scenes that should have been cut.", "Negative", 0.13),
    ("This horror film was not scary at all, just annoying.", "Negative", 0.07),
    ("A forgettable movie that offers nothing new to the genre.", "Negative", 0.14),
    # Mixed/borderline reviews
    ("The movie had its moments but was inconsistent overall.", "Negative", 0.40),
    ("Decent acting but the story lacked a clear direction.", "Negative", 0.35),
    ("Some good scenes but the pacing really hurt the film.", "Negative", 0.38),
    ("Not the worst movie but certainly not worth the hype.", "Negative", 0.42),
    ("The first half was great but the second half fell apart.", "Negative", 0.45),
    ("Visually impressive but emotionally hollow throughout.", "Negative", 0.32),
    ("An okay film that could have been much better with editing.", "Positive", 0.52),
    ("Enjoyable popcorn flick, nothing deep but entertaining.", "Positive", 0.58),
    ("The lead performance saved an otherwise mediocre script.", "Positive", 0.55),
    ("A watchable movie but not one I would see again.", "Positive", 0.53),
]

# Generate timestamps spread across multiple days
base_time = datetime(2026, 2, 25, 9, 0, 0)
records = []

for i, (review, sentiment, confidence) in enumerate(reviews_data):
    offset_hours = i * 1.1 + random.uniform(0, 1.5)
    ts = base_time + timedelta(hours=offset_hours)
    confidence_jitter = confidence + random.uniform(-0.02, 0.02)
    confidence_jitter = max(0.0, min(1.0, round(confidence_jitter, 4)))

    records.append({
        "timestamp": ts.isoformat(),
        "review": review,
        "sentiment": sentiment,
        "confidence": confidence_jitter,
        "review_length": len(review.split())
    })

csv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "api", "predictions_log.csv")
df = pd.DataFrame(records)
df.to_csv(csv_path, index=False)
print(f"Generated {len(records)} movie review predictions")
print(f"  Positive: {len([r for r in records if r['sentiment'] == 'Positive'])}")
print(f"  Negative: {len([r for r in records if r['sentiment'] == 'Negative'])}")
print(f"  Saved to: {csv_path}")
