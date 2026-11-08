"""DevPilot AI — portfolio-ready Streamlit dashboard."""
import html
import json
import sys
from pathlib import Path

import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from frontend.service import analyze_code, save_report, load_reports, optional_ai

st.set_page_config(page_title='DevPilot AI | Autonomous Software Engineer', page_icon='⚡', layout='wide', initial_sidebar_state='expanded')

for key, default in {'theme': 'Dark', 'history': [], 'latest': None, 'code': 'def calculate_total(a, b):\n    return a + b\n\nprint(undefined_variable)\n', 'request': 'Review the Python code, explain problems and suggest fixes.'}.items():
    if key not in st.session_state:
        st.session_state[key] = default

dark = st.session_state.theme == 'Dark'
bg, panel, text, muted, border = ('#090e1b','#141d30','#f1f5ff','#a4b0c7','#28364f') if dark else ('#f5f7fc','#ffffff','#172139','#64748b','#dfe5f1')
st.markdown(f'''<style>
.stApp {{background:{bg};color:{text};}}
[data-testid="stSidebar"] {{background:{panel};border-right:1px solid {border};}}
.block-container {{max-width:1420px;padding-top:2rem;padding-bottom:4rem;}}
.hero {{padding:34px 36px;border-radius:22px;background:linear-gradient(115deg,#3430a6,#5a39b5 55%,#2453a4);color:white;margin-bottom:24px;box-shadow:0 18px 40px #080e3026;}}
.hero h1 {{font-size:clamp(1.7rem,3vw,2.8rem);margin:0 0 9px;font-weight:800;letter-spacing:-1px;color:white;}}
.hero p {{margin:0;color:#e1e7ff;font-size:1rem;}}
.metric {{padding:21px;border-radius:16px;background:{panel};border:1px solid {border};min-height:126px;}}
.metric .label {{color:{muted};font-size:13px;font-weight:600;}}
.metric .value {{color:{text};font-size:29px;font-weight:800;margin-top:12px;}}
.feature {{padding:22px;border-radius:16px;background:{panel};border:1px solid {border};margin:8px 0;min-height:145px;}}
.feature h3 {{color:{text};font-size:18px;margin:0 0 10px;}}
.feature p {{color:{muted};font-size:14px;margin:0;line-height:1.6;}}
[data-testid="stMetric"] {{background:{panel};padding:15px;border:1px solid {border};border-radius:13px;}}
</style>''', unsafe_allow_html=True)

with st.sidebar:
    st.markdown('## ⚡ DevPilot AI')
    st.caption('AUTONOMOUS SOFTWARE ENGINEER')
    st.divider()
    page = st.radio('Navigation', ['🏠 Overview', '⌨️ Code Workspace', '🧠 AI Agents', '📚 RAG Knowledge', '📊 Reports', '⚙️ Settings'], label_visibility='collapsed')
    st.divider()
    st.session_state.theme = st.selectbox('Appearance', ['Dark', 'Light'], index=0 if dark else 1)
    st.caption('Python · Qwen 2.5 · FAISS · Ruff · Bandit')
    st.caption('Local-first demo · No code execution')

def metric(label, value):
    st.markdown(f'<div class="metric"><div class="label">{html.escape(str(label))}</div><div class="value">{html.escape(str(value))}</div></div>', unsafe_allow_html=True)

def feature(title, description):
    st.markdown(f'<div class="feature"><h3>{html.escape(title)}</h3><p>{html.escape(description)}</p></div>', unsafe_allow_html=True)

def render_review(result):
    counts = result['counts']
    c1, c2, c3, c4 = st.columns(4)
    with c1: st.metric('Syntax errors', counts['syntax'])
    with c2: st.metric('Quality findings', counts['quality'])
    with c3: st.metric('Security findings', counts['security'])
    with c4: st.metric('Status', result['status'].title())
    if result['tool_errors']:
        st.warning('Some checks could not run. Install missing dependencies to enable all analyzers.')
        with st.expander('Analyzer diagnostics'):
            st.json(result['tool_errors'])
    a,b,c = st.tabs(['🔍 Syntax', '🧹 Ruff', '🛡️ Bandit'])
    with a:
        if result['syntax']['status'] == 'success': st.success('Valid Python syntax')
        else: st.error('Syntax errors detected')
        st.json(result['syntax'])
    with b:
        if not result['quality']: st.info('No quality findings returned.')
        else:
            for issue in result['quality']:
                loc = issue.get('location') or {}
                st.markdown(f"**{issue.get('code','Rule')}** · Line {loc.get('row','?')} — {issue.get('message','')}")
        with st.expander('Raw Ruff results'): st.json(result['quality'])
    with c:
        if not result['security']: st.info('No security findings returned.')
        else:
            for issue in result['security']:
                st.markdown(f"**{issue.get('test_id','Rule')}** · {issue.get('issue_severity','?')} · Line {issue.get('line_number','?')} — {issue.get('issue_text','')}")
        with st.expander('Raw Bandit results'): st.json(result['security'])
    st.caption('Static checks only. Findings do not prove code is safe or correct. Submitted code was not executed.')

if page == '🏠 Overview':
    st.markdown('<div class="hero"><h1>Build better code with AI agents.</h1><p>Plan, inspect, explain and improve Python projects — all in one intelligent workspace.</p></div>', unsafe_allow_html=True)
    c1,c2,c3,c4 = st.columns(4)
    with c1: metric('SESSION ANALYSES', len(st.session_state.history))
    with c2: metric('SAVED REPORTS', len(load_reports()))
    with c3: metric('AI ENGINE', 'Qwen 2.5')
    with c4: metric('KNOWLEDGE', 'FAISS RAG')
    st.markdown('### Engineering toolkit')
    c1,c2 = st.columns(2)
    with c1:
        feature('⌨️ Smart Code Review', 'Python syntax, Ruff linting and Bandit security scanning with detailed issue reports.')
        feature('🧠 Agentic Assistance', 'On-demand planning, explanations and AI-generated repair suggestions powered by your existing agents.')
    with c2:
        feature('📚 Retrieval-Augmented Knowledge', 'Explore your embedded Python debugging knowledge base using FAISS similarity search.')
        feature('📊 Downloadable Reports', 'Keep timestamped JSON audit trails for reviews and GitHub demo screenshots.')
    st.info('Start with Code Workspace → Run Static Analysis. Qwen features are optional and may need a first-time model download.')

elif page == '⌨️ Code Workspace':
    st.title('⌨️ AI Code Workspace')
    st.caption('Paste Python code and run real static analysis. Optional AI features are available in AI Agents.')
    st.text_input('Engineering task', key='request')
    st.text_area('Python source code', key='code', height=310)
    left,right = st.columns([2,1])
    with left:
        run = st.button('⚡ Run Static Analysis', type='primary', use_container_width=True)
    with right:
        st.download_button('⬇️ Download Source', data=st.session_state.code, file_name='reviewed_code.py', mime='text/x-python', use_container_width=True)
    if run:
        try:
            with st.spinner('Running syntax, Ruff and Bandit checks...'):
                result = analyze_code(st.session_state.code)
                report = save_report(result)
            st.session_state.latest = result
            st.session_state.history.append({'timestamp': result['timestamp'], 'counts': result['counts'], 'report': report.name})
            st.success('Analysis completed and report saved.')
        except Exception as exc:
            st.error(f'Analysis failed: {type(exc).__name__}: {exc}')
    if st.session_state.latest:
        st.markdown('### Analysis results')
        render_review(st.session_state.latest)
        st.download_button('⬇️ Download Current Report', json.dumps(st.session_state.latest, indent=2), file_name='analysis_report.json', mime='application/json')

elif page == '🧠 AI Agents':
    st.title('🧠 AI Agent Studio')
    st.caption('Optional Qwen-powered workflows. First run downloads model files; CPU generation can take time.')
    st.markdown('**Planner → Reviewer → Explainer → Fixer → Static Verifier**')
    st.warning('Generated fixes are suggestions, not verified working solutions. They are never executed by this dashboard.')
    task = st.selectbox('Choose an agent', ['Explain Issues', 'Suggest Fix', 'Create Task Plan'])
    if st.button('▶ Run Selected Agent', type='primary'):
        try:
            with st.spinner('Running the selected agent. First model load may take several minutes...'):
                mode = {'Explain Issues':'explain', 'Suggest Fix':'fix', 'Create Task Plan':'plan'}[task]
                result = optional_ai(mode, st.session_state.code, st.session_state.request)
            st.session_state.agent_result = result
            st.success('Agent finished.')
        except Exception as exc:
            st.error(f'{type(exc).__name__}: {exc}')
            st.info('Check requirements.txt, model access and available RAM. Static Analysis works independently.')
    if 'agent_result' in st.session_state:
        res = st.session_state.agent_result
        if isinstance(res, dict):
            if isinstance(res.get('suggested_code'), str):
                st.code(res['suggested_code'], language='python')
                st.download_button('Download suggested code', res['suggested_code'], 'suggested_fix.py')
            st.json(res)
        else: st.write(res)

elif page == '📚 RAG Knowledge':
    st.title('📚 RAG Knowledge Search')
    st.caption('Search the existing FAISS debugging knowledge base without generating text.')
    question = st.text_input('Ask about a Python issue', value='How do I debug a NameError in Python?')
    if st.button('🔎 Search Knowledge', type='primary'):
        try:
            with st.spinner('Loading embedding model and searching...'):
                hits = optional_ai('rag', '', question)
            if hits:
                for i,hit in enumerate(hits,1):
                    with st.expander(f'Result {i} · Similarity {hit.get("similarity", 0):.3f}', expanded=i==1):
                        st.write(hit.get('document',''))
            else: st.info('No matching documents.')
        except Exception as exc:
            st.error(f'Knowledge search unavailable: {exc}')

elif page == '📊 Reports':
    st.title('📊 Reports & History')
    st.caption('Saved JSON reports from the current and previous runs.')
    reports = load_reports()
    st.metric('Report files', len(reports))
    if not reports: st.info('Run Static Analysis to create your first report.')
    else:
        selected = st.selectbox('Choose a saved report', reports, format_func=lambda p: p.name)
        try:
            content = selected.read_text(encoding='utf-8')
            st.json(json.loads(content))
            st.download_button('⬇️ Download Report', content, selected.name, mime='application/json')
        except (ValueError, OSError) as exc: st.error(str(exc))
    st.markdown('### Current session')
    if st.session_state.history: st.dataframe(st.session_state.history, use_container_width=True)
    else: st.caption('No analyses in this browser session yet.')

else:
    st.title('⚙️ Settings & Environment')
    st.write('**Appearance:**', st.session_state.theme)
    st.write('**AI model:** Qwen/Qwen2.5-0.5B-Instruct (optional)')
    st.write('**Static analysis:** Python AST + Ruff + Bandit')
    st.write('**RAG:** FAISS + sentence-transformers')
    st.write('**Security:** User-submitted code is analyzed, not executed.')
    st.info('For local use: streamlit run frontend/app.py. Do not expose this demo publicly without authentication and deployment hardening.')
