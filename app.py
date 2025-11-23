import streamlit as st
import random
from words_data import SAT_WORDS
import json

# 페이지 설정
st.set_page_config(
    page_title="SAT 단어 학습",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 세션 상태 초기화
if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0
if 'learned_words' not in st.session_state:
    st.session_state.learned_words = set()
if 'quiz_mode' not in st.session_state:
    st.session_state.quiz_mode = False
if 'quiz_words' not in st.session_state:
    st.session_state.quiz_words = []
if 'quiz_answers' not in st.session_state:
    st.session_state.quiz_answers = {}
if 'show_answer' not in st.session_state:
    st.session_state.show_answer = False
if 'filtered_words' not in st.session_state:
    st.session_state.filtered_words = SAT_WORDS.copy()

# CSS 스타일
st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .word-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .word-title {
        font-size: 2.5rem;
        font-weight: bold;
        margin-bottom: 1rem;
    }
    .word-meaning {
        font-size: 1.5rem;
        margin: 1rem 0;
    }
    .word-example {
        font-size: 1.2rem;
        font-style: italic;
        margin-top: 1rem;
        opacity: 0.9;
    }
    .progress-bar {
        margin: 2rem 0;
    }
    .stats-box {
        background: #f0f2f6;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .quiz-question {
        background: #fff3cd;
        padding: 2rem;
        border-radius: 10px;
        border-left: 5px solid #ffc107;
        margin: 1rem 0;
    }
    </style>
""", unsafe_allow_html=True)

def get_progress():
    """학습 진도 계산"""
    total = len(st.session_state.filtered_words)
    learned = len(st.session_state.learned_words)
    return learned, total, (learned / total * 100) if total > 0 else 0

def filter_words(level_filter):
    """난이도별 단어 필터링"""
    if level_filter == "전체":
        return SAT_WORDS
    return [w for w in SAT_WORDS if w['level'] == level_filter]

def main():
    # 헤더
    st.markdown('<h1 class="main-header">📚 SAT 빈출 단어 학습</h1>', unsafe_allow_html=True)
    
    # 사이드바
    with st.sidebar:
        st.header("⚙️ 설정")
        
        # 모드 선택
        mode = st.radio(
            "학습 모드",
            ["📖 학습 모드", "🧩 퀴즈 모드"],
            key="mode_selector"
        )
        
        # 난이도 필터
        level_filter = st.selectbox(
            "난이도 선택",
            ["전체", "high", "medium"],
            key="level_filter"
        )
        
        # 필터 적용
        if st.button("필터 적용"):
            st.session_state.filtered_words = filter_words(level_filter)
            st.session_state.current_word_index = 0
            st.session_state.learned_words = set()
            st.rerun()
        
        st.divider()
        
        # 통계
        learned, total, percentage = get_progress()
        st.metric("학습한 단어", f"{learned} / {total}")
        st.progress(percentage / 100)
        st.caption(f"진도: {percentage:.1f}%")
        
        st.divider()
        
        # 초기화 버튼
        if st.button("🔄 진도 초기화"):
            st.session_state.learned_words = set()
            st.session_state.current_word_index = 0
            st.rerun()
    
    # 메인 콘텐츠
    if mode == "📖 학습 모드":
        show_learning_mode()
    else:
        show_quiz_mode()

def show_learning_mode():
    """학습 모드 표시"""
    words = st.session_state.filtered_words
    
    if not words:
        st.warning("선택한 난이도에 해당하는 단어가 없습니다.")
        return
    
    # 현재 단어
    current_index = st.session_state.current_word_index % len(words)
    current_word = words[current_index]
    
    # 단어 카드
    st.markdown(f"""
        <div class="word-card">
            <div class="word-title">{current_word['word']}</div>
            <div class="word-meaning">의미: {current_word['meaning']}</div>
            <div class="word-example">예문: {current_word['example']}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 난이도 표시
    level_color = "#ff6b6b" if current_word['level'] == 'high' else "#4ecdc4"
    st.markdown(f"**난이도:** <span style='color: {level_color}; font-weight: bold;'>{current_word['level'].upper()}</span>", unsafe_allow_html=True)
    
    # 컨트롤 버튼
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("⏮️ 이전", use_container_width=True):
            st.session_state.current_word_index = (current_index - 1) % len(words)
            st.rerun()
    
    with col2:
        if st.button("✅ 학습 완료", use_container_width=True):
            st.session_state.learned_words.add(current_word['word'])
            st.success(f"'{current_word['word']}' 학습 완료!")
            st.rerun()
    
    with col3:
        if st.button("🔀 랜덤", use_container_width=True):
            st.session_state.current_word_index = random.randint(0, len(words) - 1)
            st.rerun()
    
    with col4:
        if st.button("⏭️ 다음", use_container_width=True):
            st.session_state.current_word_index = (current_index + 1) % len(words)
            st.rerun()
    
    # 학습 완료 여부 표시
    if current_word['word'] in st.session_state.learned_words:
        st.success("✅ 이 단어를 이미 학습했습니다!")
    
    # 단어 목록
    st.divider()
    st.subheader("📋 단어 목록")
    
    # 검색 기능
    search_term = st.text_input("🔍 단어 검색", key="search_input")
    
    # 단어 그리드 표시
    words_to_show = words
    if search_term:
        words_to_show = [w for w in words if search_term.lower() in w['word'].lower() or search_term.lower() in w['meaning'].lower()]
    
    if words_to_show:
        cols = st.columns(3)
        for idx, word in enumerate(words_to_show):
            with cols[idx % 3]:
                learned_icon = "✅" if word['word'] in st.session_state.learned_words else "⭕"
                if st.button(f"{learned_icon} {word['word']}", key=f"word_btn_{word['word']}", use_container_width=True):
                    # 해당 단어로 이동
                    st.session_state.current_word_index = words.index(word)
                    st.rerun()
    else:
        st.info("검색 결과가 없습니다.")

def show_quiz_mode():
    """퀴즈 모드 표시"""
    words = st.session_state.filtered_words
    
    if not words:
        st.warning("선택한 난이도에 해당하는 단어가 없습니다.")
        return
    
    # 퀴즈 초기화
    if not st.session_state.quiz_words or st.button("🔄 새 퀴즈 시작"):
        num_questions = st.slider("문제 수 선택", 5, min(20, len(words)), 10, key="quiz_num")
        st.session_state.quiz_words = random.sample(words, min(num_questions, len(words)))
        st.session_state.quiz_answers = {}
        st.session_state.show_answer = False
        st.rerun()
    
    # 퀴즈 진행
    if st.session_state.quiz_words:
        current_quiz_index = len(st.session_state.quiz_answers)
        
        if current_quiz_index < len(st.session_state.quiz_words):
            current_word = st.session_state.quiz_words[current_quiz_index]
            
            st.markdown(f"""
                <div class="quiz-question">
                    <h2>문제 {current_quiz_index + 1} / {len(st.session_state.quiz_words)}</h2>
                    <h3 style="font-size: 2rem; color: #1f77b4;">{current_word['word']}</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # 선택지 생성
            correct_answer = current_word['meaning']
            wrong_answers = [w['meaning'] for w in random.sample([w for w in words if w['word'] != current_word['word']], 3)]
            options = [correct_answer] + wrong_answers
            random.shuffle(options)
            
            selected = st.radio(
                "의미를 선택하세요:",
                options,
                key=f"quiz_option_{current_quiz_index}"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                if st.button("✅ 답 확인", use_container_width=True):
                    st.session_state.quiz_answers[current_word['word']] = selected
                    st.session_state.show_answer = True
                    st.rerun()
            
            if st.session_state.show_answer and current_word['word'] in st.session_state.quiz_answers:
                is_correct = st.session_state.quiz_answers[current_word['word']] == correct_answer
                
                if is_correct:
                    st.success(f"✅ 정답입니다! '{correct_answer}'")
                else:
                    st.error(f"❌ 오답입니다. 정답은 '{correct_answer}'입니다.")
                
                st.info(f"💡 예문: {current_word['example']}")
                
                with col2:
                    if st.button("➡️ 다음 문제", use_container_width=True):
                        st.session_state.show_answer = False
                        st.rerun()
        else:
            # 퀴즈 결과
            show_quiz_results()

def show_quiz_results():
    """퀴즈 결과 표시"""
    correct_count = 0
    total = len(st.session_state.quiz_words)
    
    st.markdown('<h2 style="text-align: center; color: #1f77b4;">🎯 퀴즈 결과</h2>', unsafe_allow_html=True)
    
    for word in st.session_state.quiz_words:
        user_answer = st.session_state.quiz_answers.get(word['word'], '')
        is_correct = user_answer == word['meaning']
        if is_correct:
            correct_count += 1
        
        result_icon = "✅" if is_correct else "❌"
        result_color = "green" if is_correct else "red"
        
        st.markdown(f"""
            <div style="padding: 1rem; margin: 0.5rem 0; border-radius: 5px; background: {'#d4edda' if is_correct else '#f8d7da'};">
                <strong>{result_icon} {word['word']}</strong><br>
                <span style="color: {result_color};">당신의 답: {user_answer}</span><br>
                <span style="color: green;">정답: {word['meaning']}</span>
            </div>
        """, unsafe_allow_html=True)
    
    score = (correct_count / total * 100) if total > 0 else 0
    
    st.markdown("---")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("정답 수", f"{correct_count} / {total}")
    with col2:
        st.metric("점수", f"{score:.1f}%")
    with col3:
        st.metric("등급", get_grade(score))
    
    st.progress(score / 100)

def get_grade(score):
    """점수에 따른 등급 반환"""
    if score >= 90:
        return "A+"
    elif score >= 80:
        return "A"
    elif score >= 70:
        return "B"
    elif score >= 60:
        return "C"
    else:
        return "D"

if __name__ == "__main__":
    main()

