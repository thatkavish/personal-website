from app import app, db, BlogPost, Book
from datetime import datetime

def add_sample_data():
    with app.app_context():
        # Clear existing data
        BlogPost.query.delete()
        Book.query.delete()
        
        # Sample blog posts
        blog_posts = [
            BlogPost(
                title="The Future of AI in Economic Policy",
                content="""
                Artificial Intelligence is revolutionizing how we approach economic policy-making. From predictive modeling 
                to real-time data analysis, AI tools are enabling policymakers to make more informed decisions than ever before.

                Key areas where AI is making an impact:
                1. Monetary Policy Analysis
                2. Economic Forecasting
                3. Market Sentiment Analysis
                4. Policy Impact Simulation

                This intersection of AI and economics represents a fascinating frontier in both fields...
                """,
                description="Exploring how artificial intelligence is reshaping economic policy-making and decision frameworks.",
                date_posted=datetime(2024, 3, 15)
            ),
            BlogPost(
                title="Behavioral Economics Meets AI",
                content="""
                The integration of behavioral economics insights with AI systems is creating new possibilities for understanding 
                and predicting human economic behavior. This synthesis is particularly powerful in areas like:

                - Consumer Choice Modeling
                - Financial Decision-Making
                - Market Psychology
                - Nudge Theory Applications

                By combining behavioral economics principles with machine learning...
                """,
                description="Understanding the intersection of human behavior and machine learning in economic decision-making.",
                date_posted=datetime(2024, 3, 10)
            ),
            BlogPost(
                title="Stanford's AI Revolution",
                content="""
                As a student at Stanford, I've had a front-row seat to the AI transformation in academia. From research 
                methodologies to classroom experiences, AI is reshaping how we learn and conduct research.

                Notable changes include:
                - AI-assisted research methods
                - New interdisciplinary courses
                - Ethical considerations in AI
                - Collaborative AI projects

                The academic landscape is evolving rapidly...
                """,
                description="A student's perspective on the AI transformation in academia and its implications for education.",
                date_posted=datetime(2024, 3, 5)
            )
        ]

        # Sample books
        books = [
            Book(
                title="Thinking, Fast and Slow",
                author="Daniel Kahneman",
                notes="A fascinating exploration of the two systems that drive our thinking: the fast, intuitive, and emotional system 1, and the slower, more deliberative system 2. Essential reading for understanding behavioral economics.",
                date_added=datetime(2024, 3, 1)
            ),
            Book(
                title="The Age of AI",
                author="Henry Kissinger, Eric Schmidt, Daniel Huttenlocher",
                notes="A thought-provoking analysis of how AI is reshaping human society, knowledge, politics, and the nature of intelligence itself.",
                date_added=datetime(2024, 2, 15)
            ),
            Book(
                title="Economics in One Lesson",
                author="Henry Hazlitt",
                notes="A clear and engaging introduction to economic thinking, emphasizing the importance of considering both immediate and long-term effects of economic policies.",
                date_added=datetime(2024, 2, 1)
            ),
            Book(
                title="Superintelligence",
                author="Nick Bostrom",
                notes="A deep dive into the potential future of artificial intelligence and its implications for humanity. Particularly relevant for understanding AI safety and ethics.",
                date_added=datetime(2024, 1, 15)
            )
        ]

        # Add to database
        db.session.add_all(blog_posts)
        db.session.add_all(books)
        db.session.commit()

if __name__ == '__main__':
    add_sample_data()
    print("Sample data added successfully!")
