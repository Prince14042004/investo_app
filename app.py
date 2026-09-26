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
    st.session_state.selected_student = "Aditya"
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
    {"title": "The ₹500 SIP That Became a Habit: Ananya's Quiet Bet on Discipline", "time": "4 min read", "excerpt": "How a simple ₹500 monthly investment grew into a ₹34,000 portfolio.", "content": """Ananya Krishnan was a second-year commerce student in Chennai when her father gave her ₹500 and one instruction: "Put this into a mutual fund SIP every month, and don't touch it, no matter what." She didn't fully understand what a SIP was, but she opened an account, picked a simple index fund, and set up an auto-debit.\n\nFor the first year, nothing exciting happened. The market dipped during her second semester, and her ₹6,000 investment briefly showed as ₹5,400. She almost cancelled the SIP out of panic. Instead, she asked a professor about it, who explained the idea of rupee-cost averaging — that a falling market meant her fixed ₹500 was now buying more units, not fewer.\n\nShe kept going. By the time she graduated, four years later, she'd invested ₹24,000 in small monthly instalments — and it had grown to just over ₹34,000, without her ever making a single "smart" trade.\n\n**The lesson:** Ananya's story isn't dramatic, and that's the point. She didn't pick a winning stock or time the market. She understood one concept — compounding through consistency — and let time do the work. Most successful student investors don't have secret knowledge; they have patience and a basic grasp of how their money grows."""},
    {"title": "How Rohan Mehta Lost His Semester's Book Fund Chasing a Telegram Tip", "time": "4 min read", "excerpt": "The harsh reality of 'guaranteed' profits and pump-and-dump schemes.", "content": """Rohan Mehta was in his final year of engineering in Pune when he joined a "stock tips" Telegram group with 40,000 members. The admin posted a small-cap chemical stock, calling it "the next multibagger" with screenshots of past picks that had apparently doubled overnight.\n\nRohan didn't check the company's financials, its promoter history, or even what the business actually did. He borrowed ₹15,000 from his book and mess fund, opened a trading app, and bought in — convinced he'd sell within a week for a quick profit.\n\nThe stock rose 8% on day one. He didn't sell, expecting more. Over the next ten days, it fell steadily as the group's "insiders" quietly exited their own positions, a classic pump-and-dump pattern. Rohan held on, refreshing the app daily, until the stock had dropped 60%. He eventually sold at a loss of nearly ₹9,000 — money he then had to explain to his parents.\n\n**The lesson:** Rohan's mistake wasn't bad luck; it was treating an anonymous tip as research. He never checked the company's basics, never questioned why strangers would freely share "guaranteed" profits, and invested money he couldn't afford to lose. A five-minute check of the company's fundamentals — or simply asking "why would this admin give away free money?" — would have saved him the loss."""},
    {"title": "From Canteen Savings to Nifty ETFs: Priya Subramaniam's Lesson in Diversification", "time": "4 min read", "excerpt": "Why skipping canteen snacks to buy into India's top 50 companies is a great beginner strategy.", "content": """Priya Subramaniam, a second-year student in Bengaluru, started by skipping the canteen twice a week and putting that ₹200 aside. Within six months she had ₹4,800 saved and no idea what to do with it — until a friend's brother, who worked in finance, showed her the concept of an index fund.\n\nInstead of trying to pick individual stocks — something she readily admitted she knew nothing about — she invested in a Nifty 50 ETF, which meant she effectively owned a small slice of India's top 50 companies at once. If one company did badly, it barely moved her overall investment, because the other 49 balanced it out.\n\nOver the next two years, as she added her savings periodically, she watched her portfolio grow steadily alongside the broader market, without the stress of tracking any single company's news.\n\n**The lesson:** Priya's advantage wasn't stock-picking skill — she had none — but she understood that spreading risk across many companies protects a beginner from the damage one bad pick can do. For someone starting out with limited knowledge, diversification is often more valuable than conviction."""},
    {"title": "The Options Trade That Ate Arjun Malhotra's Laptop Fund", "time": "4 min read", "excerpt": "A painful lesson in derivatives, expiry dates, and gambling with money you actually need.", "content": """Arjun Malhotra, a final-year student in Delhi, had saved ₹40,000 over a year specifically to buy a laptop for job interviews and internships. A YouTube video convinced him that "options trading" could double that amount in weeks, showing screenshots of the creator's own supposed profits.\n\nWithout understanding what an options contract actually was — its expiry, its leverage, or how quickly its value could hit zero — Arjun bought a batch of weekly Nifty options based on a "strategy" he'd copied from the video's comments section. The trade moved against him within two days. Because options have an expiry date and lose value fast as that date approaches, his ₹40,000 wasn't just down — it was gone entirely by the end of the week, since the contracts expired worthless.\n\nHe didn't buy a laptop that year and borrowed one from a cousin for his interviews instead.\n\n**The lesson:** Arjun's error was using money he needed for something specific to gamble on a product — derivatives — that even experienced traders find difficult to use profitably. Options aren't a faster version of investing; they're a different, much riskier instrument that can lose 100% of its value quickly. Money earmarked for a real need should never go into something this volatile."""},
    {"title": "Diversify or Die: How Fatima Sheikh Turned One Bad Pick Into a Better Strategy", "time": "4 min read", "excerpt": "Turning a 35% loss into a masterclass on reading quarterly reports and spreading risk.", "content": """Fatima Sheikh, an MBA student in Hyderabad, put her entire ₹20,000 savings into a single textile stock a classmate recommended, convinced by his confident explanation of the company's "upcoming export deal." She didn't verify the deal, and it never materialized — the stock fell 35% over three months.\n\nRather than exiting in frustration, Fatima treated the loss as a case study. She read the stock's quarterly reports for the first time, noticed the company's debt levels were high, and realized she'd invested based entirely on a friend's confidence rather than any figures of her own. She sold at a loss, but used the experience to build a small, spread-out portfolio across four sectors instead of one stock, and began reading basic annual reports before investing again.\n\nA year later, her diversified portfolio was modestly positive overall, even though one of her four picks still underperformed.\n\n**The lesson:** Fatima's story shows that a bad investment isn't always a wasted one — if it teaches the right lesson. The mistake was concentrating everything on one unverified tip; the recovery came from learning to read basic financial statements and spreading risk going forward."""},
    {"title": "Borrowed Money, Broken Trust: Vikram Nair's Crypto Crash in Final Year", "time": "5 min read", "excerpt": "The dangerous combination of FOMO, borrowed funds, and unregulated crypto tokens.", "content": """Vikram Nair was in his final semester in Kochi when a cryptocurrency he'd never heard of started trending on his Instagram feed, with influencers claiming it would "100x by year-end." He'd never invested in anything before, didn't understand blockchain fundamentals, and had no framework for judging whether a token had any real backing.\n\nHe borrowed ₹25,000 from two hostel friends, promising to repay with "interest" once the coin rose, and invested it all in one transaction, refusing to sell even a portion when it briefly doubled because he expected more. Within three weeks, the token's value had collapsed by over 90% amid a broader crypto downturn and allegations that its developers had abandoned the project.\n\nVikram couldn't repay his friends on time, which strained both friendships permanently, and he graduated with an unresolved debt hanging over him.\n\n**The lesson:** Vikram's mistake combined several errors at once: investing borrowed money, putting it all into a single speculative asset, ignoring warning signs, and never taking profits when he had the chance. Investing with money you don't own — especially into assets with no fundamental valuation — multiplies risk in ways a first-time investor is rarely prepared to handle."""},
    {"title": "The Spreadsheet That Changed Everything: Meera Iyer's Journey", "time": "5 min read", "excerpt": "Building wealth through budgeting, emergency funds, and avoiding the noise of hot tips.", "content": """Meera Iyer entered college in Mumbai completely unfamiliar with investing, intimidated by financial news channels and unsure where to even begin. Instead of jumping into any single product, she spent her first semester building a simple spreadsheet, tracking her monthly allowance, expenses, and how much she could realistically set aside.\n\nShe started small — a recurring deposit for an emergency fund first, then a modest SIP in a large-cap fund once she had a cushion. She read one basic personal finance book a senior recommended and asked her college's finance club for clarifications rather than random online strangers. Nothing she did was clever or fast; she avoided every "hot tip" her classmates chased.\n\nBy her final year, while some classmates had cycled through crypto losses and options wipeouts, Meera had a modest but steadily growing portfolio and — more importantly — the habit and knowledge to keep building it after graduation.\n\n**The lesson:** Meera's advantage was sequencing: she built financial basics — budgeting, an emergency fund, then simple long-term investments — before ever attempting anything complex. Most student investment disasters happen when people skip this order entirely and go straight for the exciting, high-risk options first."""}
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
        st.info("🎮 **Play Scenarios**\n\nTest your instincts with 20 real-life money dilemmas.")
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
    st.write("Navigate these 20 sticky financial situations. See if you have what it takes.")
    
    scenarios = [
        {
            "title": "1. The 10x Crypto Tip",
            "q": "A friend says a new crypto token will 10x by tomorrow. You have ₹2,000 saved.",
            "options": ["Go all in! ₹2,000 to ₹20,000!", "Put in ₹500 just in case.", "Ignore them and stick to your index fund."],
            "feedback": {
                "Go all in! ₹2,000 to ₹20,000!": "Ouch! The coin was a scam. Lesson: Never invest based on hype alone. 📉",
                "Put in ₹500 just in case.": "FOMO is a trap. Even ₹500 is lost money if it's a scam. Only gamble what you can lose. ⚠️",
                "Ignore them and stick to your index fund.": "Boring but brilliant! Consistency beats casino-style gambling. 📈"
            }
        },
        {
            "title": "2. The Guaranteed IPO",
            "q": "An IPO everyone's talking about is 'guaranteed to list at a premium.' You've never checked a company's financials before.",
            "options": ["Apply with your entire semester's pocket money.", "Apply with a small amount you can afford to lose.", "Read the IPO prospectus first, then decide."],
            "feedback": {
                "Apply with your entire semester's pocket money.": "Dangerous! If it lists at a discount, you're broke for the semester. 🛑",
                "Apply with a small amount you can afford to lose.": "Better, but you're still guessing blindly based on rumors. 🤔",
                "Read the IPO prospectus first, then decide.": "Smart! Never invest in a business you don't understand. 🧠"
            }
        },
        {
            "title": "3. The Options Trading Senior",
            "q": "Your senior says he made ₹50,000 in options trading last week and offers to teach you his 'strategy.'",
            "options": ["Copy his exact trades with your savings.", "Try it with ₹200 just to 'learn.'", "Politely decline and read about options risk first."],
            "feedback": {
                "Copy his exact trades with your savings.": "RIP your savings. Options are high risk and often wipe out beginners completely. 💸",
                "Try it with ₹200 just to 'learn.'": "₹200 won't teach you much, but at least your risk is low. Still, beware the rabbit hole. 🕳️",
                "Politely decline and read about options risk first.": "Perfect. Derivatives are financial weapons of mass destruction for the untrained. 🛡️"
            }
        },
        {
            "title": "4. The Credit Card Leverage",
            "q": "Your credit card limit just got increased. A stock tip group says this is the 'buy of the decade.'",
            "options": ["Use the credit limit to invest — profits will cover the bill.", "Invest only what's already in your bank account.", "Never invest borrowed or credit money, full stop."],
            "feedback": {
                "Use the credit limit to invest — profits will cover the bill.": "Absolutely not! Debt + volatile assets = financial ruin. 🚨",
                "Invest only what's already in your bank account.": "Okay, but don't blindly trust tip groups! 🕵️‍♂️",
                "Never invest borrowed or credit money, full stop.": "The golden rule of investing. Spot on! 🏆"
            }
        },
        {
            "title": "5. The Market Correction",
            "q": "Your portfolio drops 15% in a week during a market correction.",
            "options": ["Panic-sell everything immediately.", "Sell half to 'feel safer.'", "Do nothing and let your SIP continue as planned."],
            "feedback": {
                "Panic-sell everything immediately.": "You just locked in your losses! Markets always fluctuate. 📉",
                "Sell half to 'feel safer.'": "Emotional selling hurts long-term returns. 😟",
                "Do nothing and let your SIP continue as planned.": "Yes! You're actually buying units at a discount now. Ice in your veins! 🧊"
            }
        },
        {
            "title": "6. The WhatsApp Scheme",
            "q": "A WhatsApp group promises 'assured returns of 5% per month' if you refer friends and invest.",
            "options": ["Join and invite your whole hostel wing.", "Invest a small 'test' amount first.", "Recognize this as a possible Ponzi scheme and walk away."],
            "feedback": {
                "Join and invite your whole hostel wing.": "You just dragged your friends into a Ponzi scheme. Goodbye friendships. 🚩",
                "Invest a small 'test' amount first.": "They let you win small to steal big later. It's a trap. 🪤",
                "Recognize this as a possible Ponzi scheme and walk away.": "Exactly. 'Assured returns' is the biggest red flag in finance. 🚩"
            }
        },
        {
            "title": "7. The First Stipend",
            "q": "You just got your first internship stipend of ₹15,000.",
            "options": ["Spend it all — you'll invest starting next month.", "Invest half impulsively in whatever's trending.", "Split it: emergency fund, SIP, and some for yourself."],
            "feedback": {
                "Spend it all — you'll invest starting next month.": "Lifestyle creep starts here. Pay yourself first! 🛍️",
                "Invest half impulsively in whatever's trending.": "Good intention, terrible execution. 🎲",
                "Split it: emergency fund, SIP, and some for yourself.": "The holy trinity of personal finance. Nailed it! ✨"
            }
        },
        {
            "title": "8. The NFT Craze",
            "q": "Your classmate says NFTs of a random cartoon are about to explode in value.",
            "options": ["Buy several with your textbook budget.", "Buy just one to 'not miss out.'", "Skip it — you don't understand the asset, so you don't buy it."],
            "feedback": {
                "Buy several with your textbook budget.": "Enjoy explaining why you can't afford books while holding a digital JPEG. 🖼️",
                "Buy just one to 'not miss out.'": "FOMO strikes again. Don't buy what you don't understand. 🤷‍♂️",
                "Skip it — you don't understand the asset, so you don't buy it.": "Warren Buffett's favorite rule: stay in your circle of competence. 🎯"
            }
        },
        {
            "title": "9. The Gold Family Advice",
            "q": "Gold prices dip slightly and your family suggests buying gold ETFs as a student.",
            "options": ["Ignore it — gold's boring, chase the crypto instead.", "Put in a token amount without understanding ETFs.", "Research gold ETFs as a small part of a diversified plan."],
            "feedback": {
                "Ignore it — gold's boring, chase the crypto instead.": "Boring is often profitable, whereas crypto is wildly volatile. 🎢",
                "Put in a token amount without understanding ETFs.": "Blind investing isn't a strategy, even if it's family advice. 🙈",
                "Research gold ETFs as a small part of a diversified plan.": "Smart! Gold is a hedge, not a get-rich-quick scheme. 🥇"
            }
        },
        {
            "title": "10. The 'AI' Forex App",
            "q": "A 'forex trading' app promises to turn ₹1,000 into ₹10,000 in a month using an 'AI algorithm.'",
            "options": ["Deposit your savings — the app has 4.9 stars on the Play Store.", "Try the minimum deposit to 'test the algorithm.'", "Check if the app is SEBI-registered before touching it — and walk away when it isn't."],
            "feedback": {
                "Deposit your savings — the app has 4.9 stars on the Play Store.": "Reviews can be faked easily. Your lost money is very real. 📉",
                "Try the minimum deposit to 'test the algorithm.'": "They are phishing for your banking details and data. 🎣",
                "Check if the app is SEBI-registered before touching it — and walk away when it isn't.": "Excellent due diligence! SEBI protects you from scammers. 🛡️"
            }
        },
        {
            "title": "11. The Insider Info",
            "q": "Your friend's stock tip (based on 'insider info' from his uncle) is up 20% in two days. You didn't buy in initially.",
            "options": ["Buy in now at the higher price, afraid of missing more gains.", "Wait and watch, doing basic research on the company first.", "Ignore it entirely — insider tips are often illegal and unreliable."],
            "feedback": {
                "Buy in now at the higher price, afraid of missing more gains.": "You are buying at the absolute top just before the dump. 🏔️",
                "Wait and watch, doing basic research on the company first.": "Better, but remember trading on real insider info is actually illegal! ⚖️",
                "Ignore it entirely — insider tips are often illegal and unreliable.": "100% correct. Keep your hands clean and your portfolio safe. 🧼"
            }
        },
        {
            "title": "12. The Exciting NFO",
            "q": "You have ₹5,000 and no emergency fund, but a 'limited time' mutual fund NFO looks exciting.",
            "options": ["Invest the full ₹5,000 in the NFO.", "Split it between the NFO and savings.", "Build your emergency fund first; invest later once you have a cushion."],
            "feedback": {
                "Invest the full ₹5,000 in the NFO.": "If your laptop breaks tomorrow, you'll be forced to sell at a loss. 💻",
                "Split it between the NFO and savings.": "Half-measures. Emergencies don't care about your NFO. 🚑",
                "Build your emergency fund first; invest later once you have a cushion.": "Safety first! The market will always have new opportunities. 🏦"
            }
        },
        {
            "title": "13. The Unofficial Fund Manager",
            "q": "A senior offers to 'manage your money' for a cut of the profits, no paperwork, just trust.",
            "options": ["Hand over your savings — he seems experienced.", "Give him a small amount to test the arrangement.", "Decline — never give control of your money to an unregulated individual."],
            "feedback": {
                "Hand over your savings — he seems experienced.": "Kiss your money goodbye. Never, ever do this. 💸",
                "Give him a small amount to test the arrangement.": "Why pay someone to gamble your money? Learn to do it yourself. 📖",
                "Decline — never give control of your money to an unregulated individual.": "Spot on. You are your own best fund manager right now. 🦸‍♂️"
            }
        },
        {
            "title": "14. Chasing Past Returns",
            "q": "You read that a certain small-cap stock 'doubled in a month' last year and could repeat it.",
            "options": ["Buy in expecting the same pattern to repeat.", "Buy a token amount, hoping for some of the upside.", "Understand that past performance doesn't predict future returns, and research current fundamentals instead."],
            "feedback": {
                "Buy in expecting the same pattern to repeat.": "Classic mistake! Past performance does not guarantee future results! 🚫",
                "Buy a token amount, hoping for some of the upside.": "Still gambling, just with slightly less money. 🎰",
                "Understand that past performance doesn't predict future returns, and research current fundamentals instead.": "Textbook smart investing. 📚"
            }
        },
        {
            "title": "15. The Startup 'Equity'",
            "q": "Your college fest needs sponsorship, and a startup offers 'equity' in exchange for a personal loan from you.",
            "options": ["Lend your savings for a slice of an unlisted startup.", "Offer a token amount as a favor to a friend running it.", "Decline — evaluating unlisted startup risk needs expertise you don't have yet."],
            "feedback": {
                "Lend your savings for a slice of an unlisted startup.": "90% of startups fail. Your loan is gone. 📉",
                "Offer a token amount as a favor to a friend running it.": "Treat it as a donation to a friend, not a financial investment. 🤝",
                "Decline — evaluating unlisted startup risk needs expertise you don't have yet.": "Very mature decision. Stick to regulated markets for now. 🏛️"
            }
        },
        {
            "title": "16. The Herd Mentality",
            "q": "You get a ₹2,000 refund and your friends are all buying the same trending stock.",
            "options": ["Buy it just because everyone else is.", "Buy a small amount to 'not feel left out.'", "Check the company's basics independently before deciding anything."],
            "feedback": {
                "Buy it just because everyone else is.": "Herd mentality is exactly how bubbles burst on retail investors. 🐑",
                "Buy a small amount to 'not feel left out.'": "Don't let peer pressure dictate your portfolio. 🛑",
                "Check the company's basics independently before deciding anything.": "Independent thinking is an investor's greatest asset. 🧠"
            }
        },
        {
            "title": "17. The Finfluencer",
            "q": "A 'financial influencer' says 'index funds are for boring people — do this 3-stock strategy instead' in a viral reel.",
            "options": ["Switch your whole SIP into his 3 recommended stocks.", "Add a small side investment in his picks alongside your SIP.", "Recognize entertainment content isn't personalized advice, and stay the course."],
            "feedback": {
                "Switch your whole SIP into his 3 recommended stocks.": "You just outsourced your financial future to a TikToker. Bad move. 📱",
                "Add a small side investment in his picks alongside your SIP.": "A core-and-satellite strategy, but please do your own research first! 🛰️",
                "Recognize entertainment content isn't personalized advice, and stay the course.": "Yes! Finfluencers sell views, you are building real wealth. 💰"
            }
        },
        {
            "title": "18. The Brokerage Trap",
            "q": "You inherit ₹10,000 from a relative right when a 'flash sale' on a trading app offers zero brokerage for a week.",
            "options": ["Trade aggressively to make the most of the zero brokerage.", "Make a couple of small trades just to try it out.", "Treat the ₹10,000 as long-term savings, not a trading fund."],
            "feedback": {
                "Trade aggressively to make the most of the zero brokerage.": "Overtrading kills portfolios, even without brokerage fees. ☠️",
                "Make a couple of small trades just to try it out.": "The app successfully baited you into trading when you shouldn't. 🎣",
                "Treat the ₹10,000 as long-term savings, not a trading fund.": "Excellent discipline. Don't let marketing dictate your strategy. 🛡️"
            }
        },
        {
            "title": "19. The Crypto Roommate",
            "q": "Your roommate says he's quitting his part-time job because his crypto portfolio can 'cover his expenses now.'",
            "options": ["Ask him for tips and do the same.", "Keep your job but move some savings into crypto too.", "Keep your job and treat his plan as a red flag, not a role model."],
            "feedback": {
                "Ask him for tips and do the same.": "When the crypto winter hits, both of you will be completely broke. ❄️",
                "Keep your job but move some savings into crypto too.": "FOMO is tempting, but crypto shouldn't replace stable income. 🛑",
                "Keep your job and treat his plan as a red flag, not a role model.": "Very smart. Paper profits disappear fast; jobs pay the rent. 🏢"
            }
        },
        {
            "title": "20. The Study Break Trade",
            "q": "It's exam season, you're stressed, and a friend says now's the 'best time to buy the dip' in a volatile stock.",
            "options": ["Trade during your study break, chasing the dip.", "Set a small amount aside to look at 'later.'", "Focus on exams; markets will still be there after — no decision made under stress."],
            "feedback": {
                "Trade during your study break, chasing the dip.": "Stress + Investing = Disaster. And you might fail your exam! 📉",
                "Set a small amount aside to look at 'later.'": "Better, but still a distraction from your studies. 📚",
                "Focus on exams; markets will still be there after — no decision made under stress.": "Best answer. Human capital (your degree) has the highest ROI right now! 🎓"
            }
        }
    ]
    
    # Dropdown to select scenario
    scenario_titles = [s["title"] for s in scenarios]
    selected_title = st.selectbox("Select a Scenario:", scenario_titles)
    
    # Find the corresponding scenario data
    selected_scenario = next(s for s in scenarios if s["title"] == selected_title)
    
    # Clear result if scenario changes
    if 'last_scenario' not in st.session_state or st.session_state.last_scenario != selected_title:
        st.session_state.scenario_result = None
        st.session_state.last_scenario = selected_title
    
    st.markdown(f"### 🛑 {selected_scenario['q']}")
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
    st.write("Test your knowledge across 5 core investing concepts. 2 points per correct question (Max: 10).")
    
    with st.form("quiz_form"):
        st.markdown("#### **1. What is a SIP (Systematic Investment Plan)?**")
        q1 = st.radio(
            "Select your answer for Question 1:",
            [
                "A) A one-time lump sum investment in a stock",
                "B) A fixed amount invested regularly (e.g. monthly) into a mutual fund",
                "C) A type of savings account offered only to students",
                "D) A loan taken to invest in the stock market"
            ],
            index=None,
            label_visibility="collapsed"
        )
        
        st.markdown("#### **2. Why do financial advisors recommend diversification (spreading money across multiple assets)?**")
        q2 = st.radio(
            "Select your answer for Question 2:",
            [
                "A) It guarantees higher returns than any single stock",
                "B) It reduces the impact of any one investment performing badly",
                "C) It's required by law for student investors",
                "D) It eliminates all investment risk completely"
            ],
            index=None,
            label_visibility="collapsed"
        )
        
        st.markdown("#### **3. Before making any investment, what should a student ideally have in place first?**")
        q3 = st.radio(
            "Select your answer for Question 3:",
            [
                "A) A demat account with at least 5 different apps",
                "B) A small emergency fund to cover unexpected expenses",
                "C) A subscription to a paid stock tips channel",
                "D) At least ₹1 lakh in savings"
            ],
            index=None,
            label_visibility="collapsed"
        )
        
        st.markdown("#### **4. Why are options and futures (derivatives) considered risky for beginner student investors?**")
        q4 = st.radio(
            "Select your answer for Question 4:",
            [
                "A) They are illegal for anyone under 25",
                "B) They can lose their entire value quickly due to leverage and expiry dates",
                "C) They only allow investments in foreign companies",
                "D) They require a minimum investment of ₹10 lakh"
            ],
            index=None,
            label_visibility="collapsed"
        )
        
        st.markdown("#### **5. A group promises 'guaranteed 5% monthly returns' if you invest and recruit others. What is this most likely?**")
        q5 = st.radio(
            "Select your answer for Question 5:",
            [
                "A) A legitimate high-return mutual fund",
                "B) A government-backed savings scheme",
                "C) A possible Ponzi or pyramid scheme",
                "D) A standard fixed deposit offer from a bank"
            ],
            index=None,
            label_visibility="collapsed"
        )
        
        submitted = st.form_submit_button("Submit Answers")
        
        if submitted:
            if not all([q1, q2, q3, q4, q5]):
                st.warning("⚠️ Please answer all 5 questions before submitting!")
            else:
                score = 0
                results = []
                
                # Check Q1
                if q1 == "B) A fixed amount invested regularly (e.g. monthly) into a mutual fund":
                    score += 2
                    results.append("✅ **Q1:** Correct! An SIP automates regular investing into mutual funds.")
                else:
                    results.append("❌ **Q1:** Incorrect. Correct Answer is **B) A fixed amount invested regularly (e.g. monthly) into a mutual fund**.")
                
                # Check Q2
                if q2 == "B) It reduces the impact of any one investment performing badly":
                    score += 2
                    results.append("✅ **Q2:** Correct! Diversification cushions your portfolio from individual company drops.")
                else:
                    results.append("❌ **Q2:** Incorrect. Correct Answer is **B) It reduces the impact of any one investment performing badly**.")
                
                # Check Q3
                if q3 == "B) A small emergency fund to cover unexpected expenses":
                    score += 2
                    results.append("✅ **Q3:** Correct! Always build an emergency fund before locking cash into market assets.")
                else:
                    results.append("❌ **Q3:** Incorrect. Correct Answer is **B) A small emergency fund to cover unexpected expenses**.")
                
                # Check Q4
                if q4 == "B) They can lose their entire value quickly due to leverage and expiry dates":
                    score += 2
                    results.append("✅ **Q4:** Correct! Leverage and expiry decay can wipe out options contracts to ₹0.")
                else:
                    results.append("❌ **Q4:** Incorrect. Correct Answer is **B) They can lose their entire value quickly due to leverage and expiry dates**.")
                
                # Check Q5
                if q5 == "C) A possible Ponzi or pyramid scheme":
                    score += 2
                    results.append("✅ **Q5:** Correct! 'Guaranteed returns' + multi-level referral recruitment is textbook Ponzi behavior.")
                else:
                    results.append("❌ **Q5:** Incorrect. Correct Answer is **C) A possible Ponzi or pyramid scheme**.")
                
                st.session_state.quiz_score = score
                if score > st.session_state.best_score:
                    st.session_state.best_score = score
                
                st.success(f"🎯 You scored {score}/10!")
                if score == 10:
                    st.balloons()
                    st.toast("🎉 Perfect score! Master Investor tier reached.")
                    
                with st.expander("📝 View Detailed Question Breakdown", expanded=True):
                    for res in results:
                        st.markdown(res)

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
            st.write("🔥 Top tier instincts! You have a firm grip on personal finance fundamentals.")
        else:
            st.write("📈 Good effort! Review the Quick Learning section and take another swing.")

elif page == "🎬 Real Interviews":
    st.title("Other Student Experiences 🎙️")
    st.write("Hear directly from students navigating the markets.")
    
    students = {
        "Aditya": "Translating classroom finance theories into real portfolio gains.",
        "Anoop": "Talks about analyzing credit controls and market trends.",
        "Shreya": "Balancing college exams and tracking the stock market.",
        "Shradha": "Talks about learning from first stock picks."
    }
    
    st.session_state.selected_student = st.selectbox(
        "Select a Student Interview:", 
        list(students.keys()), 
        index=list(students.keys()).index(st.session_state.selected_student)
    )
    
    st.markdown(f"### Interview with {st.session_state.selected_student}")
    st.write(f"*{students[st.session_state.selected_student]}*")
    
    file_name = st.session_state.selected_student + ".mp4"
    video_path = os.path.join("videos", file_name)
    
    if os.path.exists(video_path):
        st.video(video_path)
    else:
        st.info(f"🚧 Video for {st.session_state.selected_student} coming soon! (Make sure '{file_name}' is uploaded in the videos folder).")