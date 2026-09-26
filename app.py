import streamlit as st
import pandas as pd
import plotly.express as px
import os

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

# --- NAVIGATION FUNCTION ---
def go_to(page_name):
    st.session_state.page_selection = page_name

# --- SESSION STATE INITIALIZATION ---
if 'page_selection' not in st.session_state:
    st.session_state.page_selection = "🏠 Home"
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
    {
        "title": "The ₹500 SIP That Became a Habit: Ananya's Quiet Bet on Discipline", 
        "excerpt": "How a simple ₹500 monthly investment grew into a ₹34,000 portfolio.", 
        "time": "4 min read", 
        "content": """Ananya Krishnan was a second-year commerce student in Chennai when her father gave her ₹500 and one instruction: "Put this into a mutual fund SIP every month, and don't touch it, no matter what." She didn't fully understand what a SIP was, but she opened an account, picked a simple index fund, and set up an auto-debit.\n\nFor the first year, nothing exciting happened. The market dipped during her second semester, and her ₹6,000 investment briefly showed as ₹5,400. She almost cancelled the SIP out of panic. Instead, she asked a professor about it, who explained the idea of rupee-cost averaging — that a falling market meant her fixed ₹500 was now buying more units, not fewer.\n\nShe kept going. By the time she graduated, four years later, she'd invested ₹24,000 in small monthly instalments — and it had grown to just over ₹34,000, without her ever making a single "smart" trade.\n\n**The lesson:** Ananya's story isn't dramatic, and that's the point. She didn't pick a winning stock or time the market. She understood one concept — compounding through consistency — and let time do the work. Most successful student investors don't have secret knowledge; they have patience and a basic grasp of how their money grows."""
    },
    {
        "title": "How Rohan Mehta Lost His Semester's Book Fund Chasing a Telegram Tip", 
        "excerpt": "The harsh reality of 'guaranteed' profits and pump-and-dump schemes.", 
        "time": "4 min read", 
        "content": """Rohan Mehta was in his final year of engineering in Pune when he joined a "stock tips" Telegram group with 40,000 members. The admin posted a small-cap chemical stock, calling it "the next multibagger" with screenshots of past picks that had apparently doubled overnight.\n\nRohan didn't check the company's financials, its promoter history, or even what the business actually did. He borrowed ₹15,000 from his book and mess fund, opened a trading app, and bought in — convinced he'd sell within a week for a quick profit.\n\nThe stock rose 8% on day one. He didn't sell, expecting more. Over the next ten days, it fell steadily as the group's "insiders" quietly exited their own positions, a classic pump-and-dump pattern. Rohan held on, refreshing the app daily, until the stock had dropped 60%. He eventually sold at a loss of nearly ₹9,000 — money he then had to explain to his parents.\n\n**The lesson:** Rohan's mistake wasn't bad luck; it was treating an anonymous tip as research. He never checked the company's basics, never questioned why strangers would freely share "guaranteed" profits, and invested money he couldn't afford to lose. A five-minute check of the company's fundamentals — or simply asking "why would this admin give away free money?" — would have saved him the loss."""
    },
    {
        "title": "From Canteen Savings to Nifty ETFs: Priya Subramaniam's Lesson in Diversification", 
        "excerpt": "Why skipping canteen snacks to buy into India's top 50 companies is a great beginner strategy.", 
        "time": "4 min read", 
        "content": """Priya Subramaniam, a second-year student in Bengaluru, started by skipping the canteen twice a week and putting that ₹200 aside. Within six months she had ₹4,800 saved and no idea what to do with it — until a friend's brother, who worked in finance, showed her the concept of an index fund.\n\nInstead of trying to pick individual stocks — something she readily admitted she knew nothing about — she invested in a Nifty 50 ETF, which meant she effectively owned a small slice of India's top 50 companies at once. If one company did badly, it barely moved her overall investment, because the other 49 balanced it out.\n\nOver the next two years, as she added her savings periodically, she watched her portfolio grow steadily alongside the broader market, without the stress of tracking any single company's news.\n\n**The lesson:** Priya's advantage wasn't stock-picking skill — she had none — but she understood that spreading risk across many companies protects a beginner from the damage one bad pick can do. For someone starting out with limited knowledge, diversification is often more valuable than conviction."""
    },
    {
        "title": "The Options Trade That Ate Arjun Malhotra's Laptop Fund", 
        "excerpt": "A painful lesson in derivatives, expiry dates, and gambling with money you actually need.", 
        "time": "4 min read", 
        "content": """Arjun Malhotra, a final-year student in Delhi, had saved ₹40,000 over a year specifically to buy a laptop for job interviews and internships. A YouTube video convinced him that "options trading" could double that amount in weeks, showing screenshots of the creator's own supposed profits.\n\nWithout understanding what an options contract actually was — its expiry, its leverage, or how quickly its value could hit zero — Arjun bought a batch of weekly Nifty options based on a "strategy" he'd copied from the video's comments section. The trade moved against him within two days. Because options have an expiry date and lose value fast as that date approaches, his ₹40,000 wasn't just down — it was gone entirely by the end of the week, since the contracts expired worthless.\n\nHe didn't buy a laptop that year and borrowed one from a cousin for his interviews instead.\n\n**The lesson:** Arjun's error was using money he needed for something specific to gamble on a product — derivatives — that even experienced traders find difficult to use profitably. Options aren't a faster version of investing; they're a different, much riskier instrument that can lose 100% of its value quickly. Money earmarked for a real need should never go into something this volatile."""
    },
    {
        "title": "Diversify or Die: How Fatima Sheikh Turned One Bad Pick Into a Better Strategy", 
        "excerpt": "Turning a 35% loss into a masterclass on reading quarterly reports and spreading risk.", 
        "time": "4 min read", 
        "content": """Fatima Sheikh, an MBA student in Hyderabad, put her entire ₹20,000 savings into a single textile stock a classmate recommended, convinced by his confident explanation of the company's "upcoming export deal." She didn't verify the deal, and it never materialized — the stock fell 35% over three months.\n\nRather than exiting in frustration, Fatima treated the loss as a case study. She read the stock's quarterly reports for the first time, noticed the company's debt levels were high, and realized she'd invested based entirely on a friend's confidence rather than any figures of her own. She sold at a loss, but used the experience to build a small, spread-out portfolio across four sectors instead of one stock, and began reading basic annual reports before investing again.\n\nA year later, her diversified portfolio was modestly positive overall, even though one of her four picks still underperformed.\n\n**The lesson:** Fatima's story shows that a bad investment isn't always a wasted one — if it teaches the right lesson. The mistake was concentrating everything on one unverified tip; the recovery came from learning to read basic financial statements and spreading risk going forward."""
    },
    {
        "title": "Borrowed Money, Broken Trust: Vikram Nair's Crypto Crash in Final Year", 
        "excerpt": "The dangerous combination of FOMO, borrowed funds, and unregulated crypto tokens.", 
        "time": "5 min read", 
        "content": """Vikram Nair was in his final semester in Kochi when a cryptocurrency he'd never heard of started trending on his Instagram feed, with influencers claiming it would "100x by year-end." He'd never invested in anything before, didn't understand blockchain fundamentals, and had no framework for judging whether a token had any real backing.\n\nHe borrowed ₹25,000 from two hostel friends, promising to repay with "interest" once the coin rose, and invested it all in one transaction, refusing to sell even a portion when it briefly doubled because he expected more. Within three weeks, the token's value had collapsed by over 90% amid a broader crypto downturn and allegations that its developers had abandoned the project.\n\nVikram couldn't repay his friends on time, which strained both friendships permanently, and he graduated with an unresolved debt hanging over him.\n\n**The lesson:** Vikram's mistake combined several errors at once: investing borrowed money, putting it all into a single speculative asset, ignoring warning signs, and never taking profits when he had the chance. Investing with money you don't own — especially into assets with no fundamental valuation — multiplies risk in ways a first-time investor is rarely prepared to handle."""
    },
    {
        "title": "The Spreadsheet That Changed Everything: Meera Iyer's Journey", 
        "excerpt": "Building wealth through budgeting, emergency funds, and avoiding the noise of hot tips.", 
        "time": "5 min read", 
        "content": """Meera Iyer entered college in Mumbai completely unfamiliar with investing, intimidated by financial news channels and unsure where to even begin. Instead of jumping into any single product, she spent her first semester building a simple spreadsheet, tracking her monthly allowance, expenses, and how much she could realistically set aside.\n\nShe started small — a recurring deposit for an emergency fund first, then a modest SIP in a large-cap fund once she had a cushion. She read one basic personal finance book a senior recommended and asked her college's finance club for clarifications rather than random online strangers. Nothing she did was clever or fast; she avoided every "hot tip" her classmates chased.\n\nBy her final year, while some classmates had cycled through crypto losses and options wipeouts, Meera had a modest but steadily growing portfolio and — more importantly — the habit and knowledge to keep building it after graduation.\n\n**The lesson:** Meera's advantage was sequencing: she built financial basics — budgeting, an emergency fund, then simple long-term investments — before ever attempting anything complex. Most student investment disasters happen when people skip this order entirely and go straight for the exciting, high-risk options first."""
    }
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
], key="page_selection")

# --- PAGE LOGIC ---

if page == "🏠 Home":
    st.title("Welcome to INVESTO 🚀")
    st.markdown("### *Investing, explained by students, for students.*")
    st.write("Finance doesn't have to be boring guys in suits yelling on TV. We are here to make it simple, relatable, and Gen-Z friendly. Every investor starts somewhere 🌱")
    
    st.write("---")
    st.subheader("Explore the App")
    c1, c2, c3 = st.columns(3)
    
    with c1:
        st.info("🎥 **Student Reels**\n\nQuick stories, mistakes, and lessons from peers.")
        st.button("Watch Reels", on_click=go_to, args=("🎥 Student Reels",), use_container_width=True)
    with c2:
        st.info("🎮 **Play Scenarios**\n\nTest your instincts with real-life money dilemmas.")
        st.button("Play Now", on_click=go_to, args=("🎮 What Would You Do?",), use_container_width=True)
    with c3:
        st.info("🏆 **Take the Quiz**\n\nFind out your Investor IQ and check the leaderboard.")
        st.button("Start Quiz", on_click=go_to, args=("🏆 Investing IQ Quiz",), use_container_width=True)

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
    
    # Construct exact filename mapping (e.g. "Prince Kushwaha" -> "prince_kushwaha.mp4")
    file_name = st.session_state.selected_student.lower().replace(" ", "_") + ".mp4"
    video_path = os.path.join("videos", file_name)
    
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.info(f"🚧 Video for {st.session_state.selected_student} coming soon! (Make sure '{file_name}' is inside the 'videos' folder).")