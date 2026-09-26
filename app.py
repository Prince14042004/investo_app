import streamlit as st
import pandas as pd
import plotly.express as px
import os
import random

# --- PAGE CONFIG ---
st.set_page_config(page_title="INVESTO | Student Investing", page_icon="💸", layout="wide")

# --- CUSTOM CSS ---
st.markdown("""
    <style>
    /* Custom Card Style */
    div.stExpander {
        border-radius: 15px !important;
        border: 2px solid #f0f2f6 !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
        background: linear-gradient(145deg, #ffffff, #f8f9fa);
    }
    div.stExpander:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 15px rgba(0,0,0,0.1);
        border-color: #ff4b4b !important;
    }
    
    /* Headers */
    h1, h2, h3 {
        font-family: 'Helvetica Neue', sans-serif;
        color: #2c3e50;
    }
    
    /* Highlight text */
    .highlight {
        color: #ff4b4b;
        font-weight: bold;
    }
    </style>
""", unsafe_allow_html=True)

# --- SESSION STATE INITIALIZATION ---
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = None
if 'best_score' not in st.session_state:
    st.session_state.best_score = 0
if 'selected_student' not in st.session_state:
    st.session_state.selected_student = "Prince Kushwaha"
if 'scenario_result' not in st.session_state:
    st.session_state.scenario_result = None

# --- DUMMY DATA ---
reels_data = [
    {"name": "Pratiksha", "story": "Bought random crypto at 2 AM.", "mistake": "Listened to a Twitter guru.", "lesson": "Do your own research (DYOR)!"},
    {"name": "Rohan", "story": "Put my whole allowance into one stock.", "mistake": "Zero diversification.", "lesson": "Don't put all eggs in one basket."},
    {"name": "Viplove", "story": "Started a ₹500 SIP.", "mistake": "Waited too long to start.", "lesson": "Time in the market > timing the market."},
    {"name": "Aarav", "story": "Panic sold when the market dipped 5%.", "mistake": "Letting emotions win.", "lesson": "Volatility is normal. Hold steady."},
    {"name": "Priya", "story": "Tried day trading during lectures.", "mistake": "Got distracted and lost ₹2000.", "lesson": "Investing should be passive for students."},
    {"name": "Prince", "story": "Researched Ashtavinayak fundamentals.", "mistake": "Overanalyzed and missed the entry.", "lesson": "Perfection is the enemy of action."}
]

blogs_data = [
    {"title": "My First ₹500 SIP: A Journey", "excerpt": "How skipping two coffees a month started my portfolio.", "time": "3 min read", "content": "Hey guys! So I used to spend all my pocket money by the 15th of the month. Then I discovered Mutual Funds. Setting up a ₹500 SIP was the best thing I did in my first year."},
    {"title": "FOMO into Stocks: A Horror Story", "excerpt": "I bought at the all-time high because everyone else did.", "time": "4 min read", "content": "We've all been there. My friend said a certain tech stock was going to the moon. Spoiler alert: it crashed to the earth. Always stick to your own financial plan!"},
    {"title": "From PGDM Finance to Real Portfolios", "excerpt": "Translating classroom theories into real market gains.", "time": "5 min read", "content": "Learning about exponential smoothing and vendor ratings at SIES is great, but applying financial analysis to my own portfolio hit different. Here is how I bridge the gap..."}
]

leaderboard_data = [
    {"name": "Riya K.", "score": 10},
    {"name": "Prince K.", "score": 8},
    {"name": "Viplove S.", "score": 6},
    {"name": "Pratiksha K.", "score": 4}
]

# --- SIDEBAR NAVIGATION ---
st.sidebar.title("INVESTO 💸")
st.sidebar.markdown("*Investing, explained by students, for students.*")
st.sidebar.write("---")
page = st.sidebar.radio("Navigate", [
    "🏠 Home", 
    "🎥 Student Reels", 
    "📝 Blogs", 
    "🎮 What Would You Do?", 
    "🧠 Quick Learning", 
    "🏆 Investing IQ Quiz",
    "🎬 Real Interviews"
])

# --- PAGE LOGIC ---

if page == "🏠 Home":
    st.title("Welcome to INVESTO 🚀")
    st.markdown("### *Investing, explained by students, for students.*")
    st.write("Finance doesn't have to be boring guys in suits yelling on TV. We are here to make it simple, relatable, and Gen-Z friendly. Every investor starts somewhere 🌱")
    
    st.write("---")
    st.subheader("Explore the App")
    c1, c2, c3 = st.columns(3)
    with c1:
        with st.expander("🎥 Student Reels", expanded=True):
            st.write("Quick stories, mistakes, and lessons from peers.")
    with c2:
        with st.expander("🎮 Play Scenarios", expanded=True):
            st.write("Test your instincts with real-life money dilemmas.")
    with c3:
        with st.expander("🏆 Take the Quiz", expanded=True):
            st.write("Find out your Investor IQ and check the leaderboard.")

elif page == "🎥 Student Reels":
    st.title("Student Investor Reels 📱")
    st.write("Real mistakes. Real lessons. No judgment here.")
    
    cols = st.columns(3)
    for i, reel in enumerate(reels_data):
        col = cols[i % 3]
        with col:
            with st.expander(f"👤 {reel['name']}'s Story"):
                st.markdown(f"**The Vibe:** {reel['story']}")
                st.markdown(f"📉 **Mistake:** {reel['mistake']}")
                st.markdown(f"💡 **Lesson:** {reel['lesson']}")

elif page == "📝 Blogs":
    st.title("Student Blogs ✍️")
    st.write("Read deep-dives into student finance experiences.")
    
    for blog in blogs_data:
        with st.expander(f"📖 {blog['title']} ({blog['time']})"):
            st.markdown(f"*{blog['excerpt']}*")
            st.write("---")
            st.write(blog['content'])

elif page == "🎮 What Would You Do?":
    st.title("What Would You Do? 🤔")
    st.write("Navigate these sticky financial situations.")
    
    scenarios = [
        {
            "q": "Your friend says a new crypto token will 10x by tomorrow. You have ₹2000 saved.",
            "options": ["Go all in! ₹2000 to ₹20,000!", "Put in ₹500 just in case.", "Ignore them and stick to your index fund."],
            "feedback": {
                "Go all in! ₹2000 to ₹20,000!": "Ouch! The coin was a scam. Lesson: Never invest based on hype alone. 📉",
                "Put in ₹500 just in case.": "Not terrible, but FOMO is dangerous. Lesson: Only gamble what you can lose. ⚠️",
                "Ignore them and stick to your index fund.": "Boring but brilliant! Lesson: Consistency beats casino-style gambling. 📈"
            }
        },
        {
            "q": "You get a ₹5000 birthday gift from your relatives. What's the move?",
            "options": ["Blow it all on shoes.", "Save 100% in a savings account.", "Spend ₹2000, Invest ₹3000."],
            "feedback": {
                "Blow it all on shoes.": "Drip is temporary, compounding is forever. Try saving a little next time! 👟",
                "Save 100% in a savings account.": "Great discipline! But inflation is eating your money. Look into investing it! 🏦",
                "Spend ₹2000, Invest ₹3000.": "Perfect balance! You enjoy life today while building wealth for tomorrow. ⚖️"
            }
        }
    ]
    
    selected_scenario = scenarios[0] 
    
    st.markdown(f"### 🛑 Scenario: {selected_scenario['q']}")
    choice = st.radio("Choose your move:", selected_scenario['options'], index=None)
    
    if st.button("Lock in my answer"):
        if choice:
            st.session_state.scenario_result = selected_scenario['feedback'][choice]
        else:
            st.warning("Pick an option first!")
            
    if st.session_state.scenario_result:
        st.info(st.session_state.scenario_result)

elif page == "🧠 Quick Learning":
    st.title("Quick Learning 📚")
    st.write("Jargon-free zone. Finance concepts explained like you're 5.")
    
    c1, c2 = st.columns(2)
    with c1:
        with st.expander("📈 What is an SIP?"):
            st.write("**Systematic Investment Plan.** Like a Netflix subscription, but instead of buying movies, you're buying a piece of your future every month.")
        with st.expander("🧺 Diversification"):
            st.write("Don't put all your eggs in one basket. If one stock drops, the others keep you afloat.")
    with c2:
        with st.expander("🔥 Compounding"):
            st.write("Interest making interest. It's a snowball rolling down a hill, getting bigger over time.")
        with st.expander("💸 Inflation"):
            st.write("Why a vada pav costs ₹15 today instead of ₹5. Your money loses value over time if it's not growing.")
            
    st.write("---")
    st.subheader("SIP Growth Simulator 📊")
    col1, col2, col3 = st.columns(3)
    monthly_inv = col1.number_input("Monthly SIP (₹)", min_value=500, max_value=50000, value=1000, step=500)
    years = col2.slider("Years to Invest", 1, 30, 10)
    rate = col3.slider("Expected Annual Return (%)", 5, 20, 12)
    
    months = years * 12
    rate_monthly = rate / 12 / 100
    invested_amount = monthly_inv * months
    future_value = monthly_inv * (((1 + rate_monthly)**months - 1) / rate_monthly) * (1 + rate_monthly)
    
    st.markdown(f"**Total Invested:** ₹{invested_amount:,.0f} | **Estimated Future Value:** ₹{future_value:,.0f}")
    
    data = []
    current_val = 0
    for y in range(1, years + 1):
        for m in range(1, 13):
            current_val = (current_val + monthly_inv) * (1 + rate_monthly)
        data.append({"Year": y, "Value": current_val, "Type": "Portfolio Value"})
        data.append({"Year": y, "Value": monthly_inv * 12 * y, "Type": "Amount Invested"})
        
    df = pd.DataFrame(data)
    fig = px.line(df, x="Year", y="Value", color="Type", title="The Power of Compounding", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

elif page == "🏆 Investing IQ Quiz":
    st.title("Investing IQ Quiz & Leaderboard 🏅")
    st.write("Test your knowledge. 5 Questions. 2 points each.")
    
    with st.form("quiz_form"):
        q1 = st.radio("1. What does SIP stand for?", ["Standard Investment Policy", "Systematic Investment Plan", "Stock Income Portfolio"])
        q2 = st.radio("2. Which is generally considered higher risk?", ["Fixed Deposits (FDs)", "Government Bonds", "Direct Stocks"])
        q3 = st.radio("3. What fights inflation best over the long term?", ["Keeping cash in a locker", "Savings Accounts", "Equity Mutual Funds"])
        q4 = st.radio("4. 'Don't put all your eggs in one basket' refers to:", ["Compounding", "Diversification", "Liquidity"])
        q5 = st.radio("5. When the stock market crashes, a good long-term investor should:", ["Panic and sell everything", "Review, stay calm, and maybe buy more", "Delete their trading app forever"])
        
        submitted = st.form_submit_button("Submit Answers")
        
        if submitted:
            score = 0
            if q1 == "Systematic Investment Plan": score += 2
            if q2 == "Direct Stocks": score += 2
            if q3 == "Equity Mutual Funds": score += 2
            if q4 == "Diversification": score += 2
            if q5 == "Review, stay calm, and maybe buy more": score += 2
            
            st.session_state.quiz_score = score
            if score > st.session_state.best_score:
                st.session_state.best_score = score
                
            st.success(f"You scored {score}/10!")
            if score == 10:
                st.balloons()

    if st.session_state.quiz_score is not None:
        st.write("---")
        st.subheader("Leaderboard 🏆")
        st.write(f"*Your Best Score: {st.session_state.best_score}/10*")
        
        user_entry = {"name": "You (Current User)", "score": st.session_state.best_score}
        current_leaderboard = leaderboard_data + [user_entry]
        
        df_lb = pd.DataFrame(current_leaderboard)
        df_lb = df_lb.sort_values(by="score", ascending=False).reset_index(drop=True)
        df_lb.index += 1
        
        def highlight_user(row):
            if row['name'] == "You (Current User)":
                return ['background-color: #ff4b4b; color: white'] * len(row)
            return [''] * len(row)
            
        st.dataframe(df_lb.style.apply(highlight_user, axis=1), use_container_width=True)
        
        if st.session_state.best_score >= 8:
            st.write("🔥 You're in the top tier! Great financial instincts.")
        else:
            st.write("📈 Room to grow — review the Quick Learning section and try again!")

elif page == "🎬 Real Interviews":
    st.title("Other Student Experiences 🎙️")
    st.write("Hear directly from students navigating the markets.")
    
    students = {
        "Prince Kushwaha": "Translating classroom finance theories into real portfolio gains.",
        "Viplove": "Talks about analyzing credit controls and market trends.",
        "Pratiksha": "Balancing college exams at D.Y. Patil and tracking the stock market.",
        "Aarav Sharma": "Talks about losing money in his first stock pick."
    }
    
    st.session_state.selected_student = st.selectbox(
        "Select a Student Interview:", 
        list(students.keys()), 
        index=list(students.keys()).index(st.session_state.selected_student)
    )
    
    st.markdown(f"### Interview with {st.session_state.selected_student}")
    st.write(f"*{students[st.session_state.selected_student]}*")
    
    file_name = st.session_state.selected_student.lower().replace(" ", "_") + ".mp4"
    video_path = os.path.join("videos", file_name)
    
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.info("🚧 Video coming soon! The team is currently editing this interview.")