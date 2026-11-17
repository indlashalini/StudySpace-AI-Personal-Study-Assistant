
import streamlit as st
import streamlit.components.v1 as components
import re
import database
import study_features_db as feature_db
from datetime import date, datetime


feature_db.initialize_features()

# ==================================================
# PAGE CONFIGURATION
# ==================================================

st.set_page_config(
    page_title="AI Personal Study Assistant",
    page_icon="📚",
    layout="wide"
)



# ==================================================
# PREMIUM STUDYSPACE AI THEME
# ==================================================

st.markdown("""
<style>
:root {
    --ink: #172554;
    --muted: #718096;
    --accent: #635BDB;
    --accent-dark: #4F46C8;
    --surface: #FFFFFF;
    --line: #E8EAF3;
}
.stApp {
    background: linear-gradient(135deg, #F7F8FE 0%, #F2F4FC 55%, #F8F7FF 100%);
    color: var(--ink);
}
.block-container {
    max-width: 1500px;
    padding-top: 2.0rem;
    padding-bottom: 3rem;
}
[data-testid="stHeader"] {
    background: rgba(247,248,254,0.88);
}
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #171A3A 0%, #22264F 55%, #292B5C 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}
[data-testid="stSidebar"] > div:first-child {
    padding-top: 1.5rem;
}
[data-testid="stSidebar"] * {
    color: #F6F7FF;
}
[data-testid="stSidebar"] h1 {
    font-size: 1.55rem;
    font-weight: 800;
    letter-spacing: -0.5px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] {
    padding-top: 8px;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label {
    border: 1px solid transparent;
    border-radius: 11px;
    padding: 9px 11px;
    margin: 3px 0;
    transition: all .18s ease;
}
[data-testid="stSidebar"] [data-testid="stRadio"] label:hover {
    background: rgba(255,255,255,.10);
    border-color: rgba(255,255,255,.13);
}
[data-testid="stSidebar"] [data-testid="stRadio"] label p {
    color: #F6F7FF;
    font-weight: 600;
}
h1, h2, h3 {
    color: #172554;
    letter-spacing: -0.45px;
}
h1 { font-weight: 850; }
h2, h3 { font-weight: 750; }
p, label, .stMarkdown {
    line-height: 1.55;
}
[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E7E9F2;
    border-radius: 17px;
    padding: 18px 20px;
    box-shadow: 0 7px 22px rgba(35,42,90,.045);
}
[data-testid="stMetricLabel"] {
    color: #77809A;
    font-weight: 650;
}
[data-testid="stMetricValue"] {
    color: #5148C9;
    font-weight: 850;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,.92);
    border: 1px solid #E6E8F2;
    border-radius: 17px;
    box-shadow: 0 6px 20px rgba(35,42,90,.035);
}
.stButton > button, .stFormSubmitButton > button {
    border-radius: 11px;
    border: 1px solid transparent;
    background: linear-gradient(135deg,#655CE2,#5148C9);
    color: white;
    font-weight: 700;
    min-height: 2.65rem;
    transition: transform .15s ease, box-shadow .15s ease;
}
.stButton > button:hover, .stFormSubmitButton > button:hover {
    color: white;
    border-color: transparent;
    box-shadow: 0 7px 16px rgba(81,72,201,.22);
    transform: translateY(-1px);
}
.stTextInput input, .stTextArea textarea, .stNumberInput input,
[data-baseweb="select"] > div {
    border-radius: 10px;
}
.stProgress > div > div > div {
    background: linear-gradient(90deg,#746CF0,#5148C9);
    border-radius: 30px;
}
.stProgress > div > div {
    background: #E8EAF5;
    border-radius: 30px;
}
[data-testid="stExpander"] {
    border: 1px solid #E6E8F2;
    border-radius: 13px;
    background: #FFFFFF;
}
[data-testid="stAlert"] {
    border-radius: 13px;
}
hr {
    border-color: #E5E7F0;
    margin-top: 1.5rem;
    margin-bottom: 1.5rem;
}
footer { visibility: hidden; }
@media (max-width: 800px) {
    .block-container { padding: 1rem 1rem 2rem 1rem; }
}
</style>
""", unsafe_allow_html=True)


# ==================================================
# HELPER FUNCTIONS
# ==================================================

def get_deadline_value(deadline):
    """Convert a saved date into a date object safely."""
    try:
        return date.fromisoformat(deadline)
    except (ValueError, TypeError):
        return date.today()


def calculate_percentage(completed, total):
    if total == 0:
        return 0
    return int((completed / total) * 100)


# ==================================================
# SIDEBAR NAVIGATION
# ==================================================

st.sidebar.markdown(
    """
    <div style="padding:8px 4px 18px 4px;">
      <div style="font-size:1.55rem;font-weight:850;letter-spacing:-.5px;">
        📚 StudySpace AI
      </div>
      <div style="font-size:.82rem;color:#B8BCE0;margin-top:7px;">
        Your personal learning companion
      </div>
    </div>
    """,
    unsafe_allow_html=True
)
st.sidebar.markdown("---")
page = st.sidebar.radio(
    "WORKSPACE",
    [
        "Dashboard",
        "My Study Tasks",
        "Subjects & Syllabus",
        "Daily Study Tracker",
        "AI Study Planner",
        "AI Study Chatbot",
        "Quiz Generator",
        "Smart Flashcards",
        "Exam Countdown",
        "Weekly Analytics",
        "Achievements",
        "Focus Timer"
    ],
    label_visibility="visible"
)
st.sidebar.markdown("---")
st.sidebar.caption("STUDYSPACE AI  •  LEARN SMARTER")


# ==================================================
# DASHBOARD
# ==================================================

if page == "Dashboard":

    st.title("📚 Your Study Overview")
    st.caption("A clear picture of your learning progress, priorities and study momentum.")

    tasks = database.get_tasks()
    subjects = database.get_subjects()
    sessions = database.get_study_sessions()

    total_tasks = len(tasks)
    completed_tasks = sum(int(task["completed"]) for task in tasks)
    pending_tasks = total_tasks - completed_tasks
    task_percentage = calculate_percentage(completed_tasks, total_tasks)

    all_topics = []
    for subject in subjects:
        all_topics.extend(database.get_topics(subject["id"]))

    total_topics = len(all_topics)
    learned_topics = sum(int(topic["learned"]) for topic in all_topics)
    taught_topics = sum(int(topic["teacher_taught"]) for topic in all_topics)
    revision_topics = sum(int(topic["needs_revision"]) for topic in all_topics)
    syllabus_percentage = calculate_percentage(learned_topics, total_topics)

    total_minutes = sum(int(session["duration"]) for session in sessions)
    total_hours = total_minutes / 60

    st.markdown("### ✨ Learning at a glance")
    c1, c2, c3, c4 = st.columns(4)
    for col, label, value, hint in [
        (c1, "TOTAL TASKS", total_tasks, "Your study to-do list"),
        (c2, "COMPLETED", completed_tasks, "Tasks finished"),
        (c3, "PENDING", pending_tasks, "Still to work on"),
        (c4, "SUBJECTS", len(subjects), "Subjects you're learning")
    ]:
        with col:
            with st.container(border=True):
                st.caption(label)
                st.markdown(
                    f"<div style='font-size:2.35rem;font-weight:850;color:#5148C9;line-height:1.2'>{value}</div>"
                    f"<div style='font-size:.82rem;color:#77809A;margin-top:7px'>{hint}</div>",
                    unsafe_allow_html=True
                )

    st.markdown("### 🎯 Progress and consistency")
    p1, p2 = st.columns(2)
    with p1:
        with st.container(border=True):
            st.markdown("#### 📝 Task completion")
            st.markdown(f"<div style='font-size:2rem;font-weight:850;color:#5148C9'>{task_percentage}%</div>", unsafe_allow_html=True)
            st.progress(task_percentage / 100)
            st.caption(f"{completed_tasks} of {total_tasks} tasks completed")
    with p2:
        with st.container(border=True):
            st.markdown("#### 📖 Syllabus progress")
            st.markdown(f"<div style='font-size:2rem;font-weight:850;color:#5148C9'>{syllabus_percentage}%</div>", unsafe_allow_html=True)
            st.progress(syllabus_percentage / 100)
            st.caption(f"{learned_topics} of {total_topics} topics marked as learned")

    st.markdown("### 📈 Your learning statistics")
    a, b, c, d = st.columns(4)
    a.metric("Topics in syllabus", total_topics)
    b.metric("Topics taught", taught_topics)
    c.metric("Topics learned", learned_topics)
    d.metric("Needs revision", revision_topics)

    with st.container(border=True):
        st.markdown("#### ⏱️ Total recorded study time")
        st.markdown(
            f"<div style='font-size:2.1rem;font-weight:850;color:#5148C9'>{total_hours:.1f} hours</div>"
            f"<div style='color:#77809A'>{total_minutes} minutes recorded in Daily Study Tracker</div>",
            unsafe_allow_html=True
        )

    st.markdown("### 📚 Subject-wise progress")
    if subjects:
        for subject in subjects:
            topics = database.get_topics(subject["id"])
            subject_total = len(topics)
            subject_learned = sum(int(topic["learned"]) for topic in topics)
            percentage = calculate_percentage(subject_learned, subject_total)
            with st.container(border=True):
                left, right = st.columns([4, 1])
                left.markdown(f"**{subject['name']}**")
                right.markdown(
                    f"<div style='text-align:right;font-weight:800;color:#5148C9'>{percentage}%</div>",
                    unsafe_allow_html=True
                )
                st.progress(percentage / 100)
                st.caption(f"{subject_learned} of {subject_total} topics learned")
    else:
        st.info("Add your subjects in Subjects & Syllabus to begin tracking progress.")

    st.markdown("### 📌 Next tasks")
    pending_list = [task for task in tasks if not task["completed"]]
    if pending_list:
        for task in pending_list[:5]:
            with st.container(border=True):
                st.markdown(f"**{task['task']}**")
                x, y, z = st.columns(3)
                x.caption(f"📚 {task['subject']}")
                y.caption(f"📅 {task['deadline']}")
                z.caption(f"⚡ {task['priority']}")
        if len(pending_list) > 5:
            st.caption(f"{len(pending_list) - 5} more pending tasks are in My Study Tasks.")
    else:
        st.success("🎉 You're all caught up. No pending study tasks!")

elif page == "My Study Tasks":

    st.title("📝 My Study Tasks")
    st.caption("Plan your academic work, stay ahead of deadlines and celebrate completed tasks.")

    tasks = database.get_tasks()
    total = len(tasks)
    completed_count = sum(int(t["completed"]) for t in tasks)
    pending_count = total - completed_count
    completion_rate = calculate_percentage(completed_count, total)

    st.markdown("### Your task snapshot")
    c1, c2, c3, c4 = st.columns(4)
    for col, label, value in [
        (c1, "ALL TASKS", total),
        (c2, "COMPLETED", completed_count),
        (c3, "PENDING", pending_count),
        (c4, "COMPLETION", f"{completion_rate}%")
    ]:
        with col:
            with st.container(border=True):
                st.caption(label)
                st.markdown(
                    f"<div style='font-size:2rem;font-weight:850;color:#5148C9'>{value}</div>",
                    unsafe_allow_html=True
                )

    st.markdown("### ➕ Add a new task")
    with st.container(border=True):
        with st.form("add_task_form", clear_on_submit=True):
            subject = st.text_input("Subject", placeholder="e.g. Python Programming")
            task_name = st.text_input("Task description", placeholder="e.g. Complete Chapter 3 exercises")
            left, right = st.columns(2)
            with left:
                difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])
            with right:
                priority = st.selectbox("Priority", ["Low", "Medium", "High"])
            deadline = st.date_input("Deadline", value=date.today())
            add_button = st.form_submit_button("＋ Add task to my list", use_container_width=True)
            if add_button:
                if subject.strip() and task_name.strip():
                    database.add_task(
                        subject.strip(), task_name.strip(), difficulty,
                        priority, deadline.isoformat()
                    )
                    st.success("Task added successfully.")
                    st.rerun()
                else:
                    st.error("Please enter both a subject and task description.")

    st.markdown("### 📋 Your task list")
    tasks = database.get_tasks()
    if not tasks:
        st.info("Your task list is empty. Add your first task above.")
    else:
        f1, f2, f3 = st.columns([2, 1, 1])
        with f1:
            search_text = st.text_input("🔎 Search tasks", placeholder="Search subject or task")
        with f2:
            priority_filter = st.selectbox("Priority", ["All", "Low", "Medium", "High"])
        with f3:
            status_filter = st.selectbox("Status", ["All", "Pending", "Completed"])

        filtered_tasks = []
        for task in tasks:
            subject_text = str(task["subject"]).lower()
            task_text = str(task["task"]).lower()
            matches_search = search_text.lower() in subject_text or search_text.lower() in task_text
            matches_priority = priority_filter == "All" or task["priority"] == priority_filter
            is_completed = bool(task["completed"])
            matches_status = (
                status_filter == "All"
                or (status_filter == "Completed" and is_completed)
                or (status_filter == "Pending" and not is_completed)
            )
            if matches_search and matches_priority and matches_status:
                filtered_tasks.append(task)

        st.caption(f"Showing {len(filtered_tasks)} of {len(tasks)} tasks")
        if not filtered_tasks:
            st.info("No tasks match these filters. Try changing your search.")

        for task in filtered_tasks:
            with st.container(border=True):
                heading, status_col = st.columns([4, 1])
                with heading:
                    st.markdown(f"#### {task['task']}")
                    st.caption(f"📚 {task['subject']}")
                with status_col:
                    if task["completed"]:
                        st.success("Completed")
                    else:
                        st.warning("Pending")

                x, y, z = st.columns(3)
                x.caption(f"🎯 {task['difficulty']}")
                y.caption(f"⚡ {task['priority']} priority")
                z.caption(f"📅 {task['deadline']}")

                checked = st.checkbox(
                    "Mark as completed",
                    value=bool(task["completed"]),
                    key=f"task_completed_{task['id']}"
                )
                if checked != bool(task["completed"]):
                    database.update_task_status(task["id"], checked)
                    st.rerun()

                with st.expander("✏️ Edit task details"):
                    with st.form(f"edit_task_form_{task['id']}"):
                        edit_subject = st.text_input("Subject", value=task["subject"], key=f"edit_subject_{task['id']}")
                        edit_task_name = st.text_input("Task description", value=task["task"], key=f"edit_name_{task['id']}")
                        difficulty_options = ["Easy", "Medium", "Hard"]
                        priority_options = ["Low", "Medium", "High"]
                        edit_difficulty = st.selectbox(
                            "Difficulty", difficulty_options,
                            index=difficulty_options.index(task["difficulty"]) if task["difficulty"] in difficulty_options else 0,
                            key=f"edit_difficulty_{task['id']}"
                        )
                        edit_priority = st.selectbox(
                            "Priority", priority_options,
                            index=priority_options.index(task["priority"]) if task["priority"] in priority_options else 0,
                            key=f"edit_priority_{task['id']}"
                        )
                        edit_deadline = st.date_input(
                            "Deadline", value=get_deadline_value(task["deadline"]),
                            key=f"edit_deadline_{task['id']}"
                        )
                        if st.form_submit_button("Save changes", use_container_width=True):
                            if edit_subject.strip() and edit_task_name.strip():
                                database.update_task(
                                    task["id"], edit_subject.strip(), edit_task_name.strip(),
                                    edit_difficulty, edit_priority, edit_deadline.isoformat()
                                )
                                st.success("Task updated.")
                                st.rerun()
                            else:
                                st.error("Subject and task description cannot be empty.")

                with st.expander("🗑️ Delete task"):
                    confirm_delete = st.checkbox(
                        "I understand this will permanently delete this task.",
                        key=f"confirm_delete_task_{task['id']}"
                    )
                    if st.button("Delete this task", key=f"delete_task_{task['id']}", type="secondary", use_container_width=True):
                        if confirm_delete:
                            database.delete_task(task["id"])
                            st.success("Task deleted.")
                            st.rerun()
                        else:
                            st.warning("Please confirm before deleting.")

elif page == "Subjects & Syllabus":

    st.title("📚 Subjects & Syllabus")
    st.caption("Build your subject library, organise every syllabus topic and track what you have mastered.")

    subjects = database.get_subjects()

    # Overall subject and syllabus snapshot
    all_topics = []
    for subject in subjects:
        all_topics.extend(database.get_topics(subject["id"]))

    total_topics_all = len(all_topics)
    learned_all = sum(int(topic["learned"]) for topic in all_topics)
    taught_all = sum(int(topic["teacher_taught"]) for topic in all_topics)
    revision_all = sum(int(topic["needs_revision"]) for topic in all_topics)
    overall_progress = calculate_percentage(learned_all, total_topics_all)

    st.markdown("### ✨ Your learning library")
    m1, m2, m3, m4 = st.columns(4)

    for col, label, value in [
        (m1, "SUBJECTS", len(subjects)),
        (m2, "SYLLABUS TOPICS", total_topics_all),
        (m3, "TOPICS LEARNED", learned_all),
        (m4, "NEED REVISION", revision_all)
    ]:
        with col:
            with st.container(border=True):
                st.caption(label)
                st.markdown(
                    f"<div style='font-size:2rem;font-weight:850;color:#5148C9'>{value}</div>",
                    unsafe_allow_html=True
                )

    with st.container(border=True):
        pleft, pright = st.columns([3, 1])
        with pleft:
            st.markdown("#### Overall syllabus completion")
            st.progress(overall_progress / 100)
            st.caption(f"{learned_all} of {total_topics_all} topics marked as learned")
        with pright:
            st.markdown(
                f"<div style='font-size:2rem;font-weight:850;color:#5148C9;text-align:right'>{overall_progress}%</div>",
                unsafe_allow_html=True
            )

    st.markdown("### ➕ Add a subject")
    with st.container(border=True):
        with st.form("add_subject_form"):
            subject_name = st.text_input(
                "Subject name",
                placeholder="e.g. Data Structures and Algorithms"
            )
            subject_description = st.text_area(
                "Short description",
                placeholder="What will you study in this subject?",
                height=90
            )
            add_subject_button = st.form_submit_button(
                "＋ Add subject",
                use_container_width=True
            )

            if add_subject_button:
                if subject_name.strip():
                    success = database.add_subject(
                        subject_name.strip(),
                        subject_description.strip()
                    )
                    if success:
                        st.success("Subject added to your learning library.")
                        st.rerun()
                    else:
                        st.error("A subject with this name already exists.")
                else:
                    st.error("Please enter a subject name.")

    st.markdown("### 🗂️ Subject workspace")
    subjects = database.get_subjects()

    if not subjects:
        st.info("Your subject library is empty. Add your first subject above.")
    else:
        # Compact subject overview cards
        card_columns = st.columns(min(3, len(subjects)))
        for index, subject in enumerate(subjects):
            topics_for_card = database.get_topics(subject["id"])
            learned_for_card = sum(int(topic["learned"]) for topic in topics_for_card)
            subject_progress = calculate_percentage(learned_for_card, len(topics_for_card))
            with card_columns[index % len(card_columns)]:
                with st.container(border=True):
                    st.markdown(f"#### 📘 {subject['name']}")
                    st.markdown(
                        f"<div style='font-size:1.7rem;font-weight:850;color:#5148C9'>{subject_progress}%</div>",
                        unsafe_allow_html=True
                    )
                    st.progress(subject_progress / 100)
                    st.caption(f"{learned_for_card}/{len(topics_for_card)} topics learned")

        subject_options = {
            f"{subject['name']}": subject
            for subject in subjects
        }
        selected_label = st.selectbox(
            "Choose a subject to manage",
            list(subject_options.keys()),
            key="subject_workspace_selector"
        )
        selected_subject = subject_options[selected_label]
        subject_id = selected_subject["id"]
        topics = database.get_topics(subject_id)

        st.divider()
        st.markdown(f"### 📖 {selected_subject['name']}")
        if selected_subject["description"]:
            st.caption(selected_subject["description"])

        edit_col, delete_col = st.columns(2)

        with edit_col:
            with st.expander("✏️ Edit subject details"):
                with st.form(f"edit_subject_{subject_id}"):
                    edit_subject_name = st.text_input(
                        "Subject name",
                        value=selected_subject["name"]
                    )
                    edit_subject_description = st.text_area(
                        "Description",
                        value=selected_subject["description"],
                        height=90
                    )
                    update_subject_button = st.form_submit_button(
                        "Save subject changes",
                        use_container_width=True
                    )
                    if update_subject_button:
                        if edit_subject_name.strip():
                            success = database.update_subject(
                                subject_id,
                                edit_subject_name.strip(),
                                edit_subject_description.strip()
                            )
                            if success:
                                st.success("Subject details updated.")
                                st.rerun()
                            else:
                                st.error("Another subject already has this name.")
                        else:
                            st.error("Subject name cannot be empty.")

        with delete_col:
            with st.expander("🗑️ Delete subject"):
                st.warning(
                    "Deleting a subject also deletes its syllabus topics. "
                    "Study tasks and study-session records are not deleted."
                )
                confirm_subject_delete = st.checkbox(
                    "I understand and want to delete this subject.",
                    key=f"confirm_subject_delete_{subject_id}"
                )
                if st.button(
                    "Delete this subject",
                    key=f"delete_subject_{subject_id}",
                    use_container_width=True
                ):
                    if confirm_subject_delete:
                        database.delete_subject(subject_id)
                        st.success("Subject deleted.")
                        st.rerun()
                    else:
                        st.warning("Please confirm before deleting.")

        st.markdown("### ➕ Add syllabus topics")
        with st.container(border=True):
            with st.form(f"add_topic_form_{subject_id}", clear_on_submit=True):
                topic_name = st.text_input(
                    "Topic name",
                    placeholder="e.g. Introduction to Algorithms"
                )
                add_topic_button = st.form_submit_button(
                    "＋ Add topic",
                    use_container_width=True
                )
                if add_topic_button:
                    if topic_name.strip():
                        success = database.add_topic(subject_id, topic_name.strip())
                        if success:
                            st.success("Topic added to this syllabus.")
                            st.rerun()
                        else:
                            st.error("This topic already exists in this subject.")
                    else:
                        st.error("Please enter a topic name.")

        # Refresh topics after subject operations
        topics = database.get_topics(subject_id)
        total_topics = len(topics)
        taught_count = sum(int(topic["teacher_taught"]) for topic in topics)
        learned_count = sum(int(topic["learned"]) for topic in topics)
        revision_count = sum(int(topic["needs_revision"]) for topic in topics)
        syllabus_percentage = calculate_percentage(learned_count, total_topics)

        st.markdown("### 🎯 Subject progress")
        s1, s2, s3, s4 = st.columns(4)
        s1.metric("Total topics", total_topics)
        s2.metric("Teacher taught", taught_count)
        s3.metric("Learned", learned_count)
        s4.metric("Needs revision", revision_count)

        prog_left, prog_right = st.columns([4, 1])
        with prog_left:
            st.progress(syllabus_percentage / 100)
            st.caption(f"{learned_count} of {total_topics} topics learned")
        with prog_right:
            st.markdown(
                f"<div style='font-size:1.6rem;font-weight:850;color:#5148C9;text-align:right'>{syllabus_percentage}%</div>",
                unsafe_allow_html=True
            )

        st.markdown("### 📋 Topic checklist")
        if not topics:
            st.info("No topics have been added to this subject yet. Add your first topic above.")
        else:
            for topic in topics:
                with st.container(border=True):
                    title_col, state_col = st.columns([3, 1])
                    with title_col:
                        st.markdown(f"**{topic['topic_name']}**")
                    with state_col:
                        if topic["learned"]:
                            st.success("Learned")
                        elif topic["needs_revision"]:
                            st.warning("Revise")
                        elif topic["teacher_taught"]:
                            st.info("Taught")
                        else:
                            st.caption("Not started")

                    with st.form(f"topic_status_form_{topic['id']}"):
                        status_a, status_b, status_c = st.columns(3)
                        with status_a:
                            teacher_taught = st.checkbox(
                                "Teacher taught",
                                value=bool(topic["teacher_taught"])
                            )
                        with status_b:
                            learned = st.checkbox(
                                "I have learned",
                                value=bool(topic["learned"])
                            )
                        with status_c:
                            needs_revision = st.checkbox(
                                "Needs revision",
                                value=bool(topic["needs_revision"])
                            )

                        save_status = st.form_submit_button(
                            "Save progress",
                            use_container_width=True
                        )
                        if save_status:
                            database.update_topic_status(
                                topic["id"], "teacher_taught", teacher_taught
                            )
                            database.update_topic_status(
                                topic["id"], "learned", learned
                            )
                            database.update_topic_status(
                                topic["id"], "needs_revision", needs_revision
                            )
                            st.success("Topic progress saved.")
                            st.rerun()

                    with st.expander("✏️ Rename topic"):
                        with st.form(f"edit_topic_form_{topic['id']}"):
                            edited_topic_name = st.text_input(
                                "Topic name",
                                value=topic["topic_name"]
                            )
                            update_topic_button = st.form_submit_button(
                                "Save topic name",
                                use_container_width=True
                            )
                            if update_topic_button:
                                if edited_topic_name.strip():
                                    success = database.update_topic(
                                        topic["id"], edited_topic_name.strip()
                                    )
                                    if success:
                                        st.success("Topic renamed.")
                                        st.rerun()
                                    else:
                                        st.error("A topic with this name already exists.")
                                else:
                                    st.error("Topic name cannot be empty.")

                    with st.expander("🗑️ Delete topic"):
                        confirm_topic_delete = st.checkbox(
                            "Confirm that I want to delete this topic.",
                            key=f"confirm_topic_delete_{topic['id']}"
                        )
                        if st.button(
                            "Delete topic",
                            key=f"delete_topic_{topic['id']}",
                            use_container_width=True
                        ):
                            if confirm_topic_delete:
                                database.delete_topic(topic["id"])
                                st.success("Topic deleted.")
                                st.rerun()
                            else:
                                st.warning("Please confirm before deleting.")

        st.markdown("### 🔁 Revision list")
        revision_list = [topic for topic in topics if topic["needs_revision"]]
        if revision_list:
            for topic in revision_list:
                st.markdown(f"- **{topic['topic_name']}**")
        else:
            st.success("No topics in this subject are currently marked for revision.")


# ==================================================
# DAILY STUDY TRACKER
# ==================================================

elif page == "Daily Study Tracker":

    st.title("⏱️ Daily Study Tracker")

    st.write(
        "Record your study sessions and monitor "
        "the time you spend learning."
    )

    subjects = database.get_subjects()

    if not subjects:

        st.warning(
            "Please add at least one subject in "
            "the Subjects & Syllabus page first."
        )

    else:

        subject_names = [
            subject["name"] for subject in subjects
        ]

        st.subheader("Add a Study Session")

        with st.form("study_session_form"):

            selected_subject = st.selectbox(
                "Select Subject",
                subject_names
            )

            study_topic = st.text_input(
                "What did you study?",
                placeholder="Example: Python Functions and Loops"
            )

            duration = st.number_input(
                "Study Duration (minutes)",
                min_value=1,
                max_value=1440,
                value=60,
                step=5
            )

            study_date = st.date_input(
                "Study Date",
                value=date.today()
            )

            save_session = st.form_submit_button(
                "Save Study Session",
                use_container_width=True
            )

            if save_session:

                if study_topic.strip():

                    database.add_study_session(
                        selected_subject,
                        study_topic.strip(),
                        int(duration),
                        study_date.isoformat()
                    )

                    st.success("Study session saved successfully!")
                    st.rerun()

                else:
                    st.error("Please enter what you studied.")

    st.divider()

    sessions = database.get_study_sessions()

    st.subheader("Your Study Statistics")

    total_minutes = sum(
        session["duration"] for session in sessions
    )

    total_hours = total_minutes / 60

    today_string = date.today().isoformat()

    today_minutes = sum(
        session["duration"]
        for session in sessions
        if session["study_date"] == today_string
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "Total Study Hours",
        f"{total_hours:.1f} hrs"
    )

    col2.metric(
        "Total Sessions",
        len(sessions)
    )

    col3.metric(
        "Today's Study Time",
        f"{today_minutes} min"
    )

    st.divider()

    st.subheader("Study History")

    if sessions:

        for session in sessions:

            with st.container(border=True):

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.write(f"**{session['subject']}**")

                    st.write(
                        f"Topic: {session['topic']}"
                    )

                    st.write(
                        f"Date: {session['study_date']}"
                    )

                    st.write(
                        f"Duration: {session['duration']} minutes"
                    )

                with col2:

                    if st.button(
                        "Delete",
                        key=f"delete_session_{session['id']}"
                    ):

                        database.delete_study_session(
                            session["id"]
                        )

                        st.success("Study session deleted.")
                        st.rerun()

    else:

        st.info(
            "No study sessions recorded yet. "
            "Add your first session above."
        )


# ==================================================
# AI STUDY PLANNER
# ==================================================

elif page == "AI Study Planner":

    from ai_engine import generate_study_plan

    st.title("🤖 AI-Powered Study Planner")
    st.write(
        "Generate a personalized study plan using Gemini or your local "
        "Ollama model. Review the plan before adding tasks."
    )

    with st.form("ai_study_plan_form"):
        study_goal = st.text_area(
            "What do you need to study?",
            placeholder=(
                "Example: Prepare for my Python exam covering loops, "
                "functions, lists, tuples and dictionaries."
            ),
            height=110
        )

        col1, col2 = st.columns(2)
        with col1:
            exam_date = st.date_input(
                "Exam / target date",
                value=date.today()
            )
            daily_hours = st.number_input(
                "Available study hours per day",
                min_value=0.5,
                max_value=12.0,
                value=2.0,
                step=0.5
            )
        with col2:
            provider = st.selectbox(
                "AI provider",
                [
                    "Gemini",
                    "Ollama (local)",
                    "Automatic fallback (Ollama → Gemini)"
                ]
            )
            level = st.selectbox(
                "Your current level",
                ["Beginner", "Intermediate", "Advanced"]
            )

        extra_preferences = st.text_area(
            "Additional preferences (optional)",
            placeholder=(
                "Example: Include short breaks, practice questions, "
                "and revision. I prefer studying in the evening."
            ),
            height=80
        )

        create_plan = st.form_submit_button(
            "✨ Generate Study Plan",
            use_container_width=True
        )

    if create_plan:
        if not study_goal.strip():
            st.error("Please describe what you need to study.")
        else:
            with st.spinner("Your AI study plan is being generated..."):
                try:
                    plan_text, used_provider = generate_study_plan(
                        goal=study_goal.strip(),
                        target_date=exam_date.isoformat(),
                        daily_hours=float(daily_hours),
                        level=level,
                        preferences=extra_preferences.strip(),
                        provider=provider
                    )
                    st.session_state["generated_study_plan"] = plan_text
                    st.session_state["generated_study_plan_provider"] = used_provider
                    st.success(f"Study plan generated using {used_provider}.")
                except Exception as error:
                    st.error(f"Could not generate the study plan: {error}")

    if st.session_state.get("generated_study_plan"):
        st.divider()
        st.subheader("Your Generated Study Plan")
        st.caption(
            "AI-generated suggestions may need adjustment. Check dates and "
            "workload before saving anything."
        )
        st.markdown(st.session_state["generated_study_plan"])

        st.subheader("Save a task from this plan")
        subjects = database.get_subjects()
        known_subjects = [item["name"] for item in subjects]
        default_subject = known_subjects[0] if known_subjects else ""

        with st.form("save_ai_plan_task_form"):
            task_subject = st.text_input(
                "Subject",
                value=default_subject,
                placeholder="Example: Python"
            )
            task_description = st.text_input(
                "Task description",
                placeholder="Example: Revise Python loops"
            )
            col1, col2 = st.columns(2)
            with col1:
                task_difficulty = st.selectbox(
                    "Difficulty",
                    ["Easy", "Medium", "Hard"],
                    key="ai_task_difficulty"
                )
            with col2:
                task_priority = st.selectbox(
                    "Priority",
                    ["Low", "Medium", "High"],
                    index=1,
                    key="ai_task_priority"
                )
            task_deadline = st.date_input(
                "Task deadline",
                value=date.today(),
                key="ai_task_deadline"
            )
            save_ai_task = st.form_submit_button("➕ Save Task")

            if save_ai_task:
                if task_subject.strip() and task_description.strip():
                    database.add_task(
                        task_subject.strip(),
                        task_description.strip(),
                        task_difficulty,
                        task_priority,
                        task_deadline.isoformat()
                    )
                    st.success("Task saved to My Study Tasks.")
                    st.rerun()
                else:
                    st.error("Enter both a subject and task description.")

        if st.button("Clear generated plan"):
            st.session_state.pop("generated_study_plan", None)
            st.session_state.pop("generated_study_plan_provider", None)
            st.rerun()



# ==================================================
# AI STUDY CHATBOT
# ==================================================

elif page == "AI Study Chatbot":

    from ai_engine import generate_ai_text

    st.title("💬 AI Study Chatbot")
    st.write("Ask study-related questions and get explanations, examples and practice guidance.")

    provider = st.selectbox(
        "Choose AI provider",
        ["Gemini", "Ollama (local)", "Automatic fallback (Ollama → Gemini)"],
        key="chat_provider"
    )

    if "study_chat" not in st.session_state:
        st.session_state["study_chat"] = []

    for message in st.session_state["study_chat"]:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    question = st.chat_input("Ask a question about your studies...")
    if question:
        st.session_state["study_chat"].append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        conversation_context = "\n".join(
            f'{m["role"].upper()}: {m["content"]}'
            for m in st.session_state["study_chat"][-8:]
        )
        prompt = (
            "You are a friendly, accurate academic tutor. Explain concepts "
            "at a student-friendly level. Use examples and step-by-step reasoning "
            "when useful. If a question is ambiguous, ask a brief clarification. "
            "Do not invent facts.\n\nConversation:\n" + conversation_context
        )
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer, used_provider = generate_ai_text(prompt, provider)
                    st.markdown(answer)
                    st.caption(f"Answered using {used_provider}")
                    st.session_state["study_chat"].append(
                        {"role": "assistant", "content": answer}
                    )
                except Exception as error:
                    st.error(f"AI assistant error: {error}")

    if st.button("Clear chat history"):
        st.session_state["study_chat"] = []
        st.rerun()


# ==================================================
# QUIZ GENERATOR
# ==================================================

elif page == "Quiz Generator":

    from ai_engine import generate_ai_text
    import json

    st.title("🧠 AI Quiz Generator")
    st.write("Create a multiple-choice quiz, answer it, and review explanations.")

    col1, col2 = st.columns(2)
    with col1:
        quiz_topic = st.text_input("Quiz topic", placeholder="Example: Python loops")
        quiz_count = st.selectbox("Number of questions", [5, 10], index=0)
    with col2:
        quiz_level = st.selectbox("Difficulty", ["Beginner", "Intermediate", "Advanced"])
        quiz_provider = st.selectbox(
            "AI provider",
            ["Gemini", "Ollama (local)", "Automatic fallback (Ollama → Gemini)"],
            key="quiz_provider"
        )

    if st.button("Generate Quiz", type="primary"):
        if not quiz_topic.strip():
            st.warning("Enter a quiz topic first.")
        else:
            prompt = f"""
Create {quiz_count} multiple-choice questions about: {quiz_topic}.
Difficulty: {quiz_level}.
Return ONLY valid JSON, no markdown fences, in this exact format:
{{
  "questions": [
    {{
      "question": "Question text",
      "options": ["A", "B", "C", "D"],
      "answer": "A",
      "explanation": "Short explanation"
    }}
  ]
}}
The answer must exactly match one option. Include exactly {quiz_count} questions.
"""
            with st.spinner("Creating your quiz..."):
                try:
                    response, used = generate_ai_text(prompt, quiz_provider)
                    cleaned = response.strip()
                    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", cleaned, flags=re.I)
                    quiz_data = json.loads(cleaned)
                    questions = quiz_data.get("questions", [])
                    valid = [
                        q for q in questions
                        if isinstance(q, dict)
                        and isinstance(q.get("question"), str)
                        and q.get("question", "").strip()
                        and isinstance(q.get("options"), list)
                        and len(q["options"]) == 4
                        and all(isinstance(option, str) and option.strip() for option in q["options"])
                        and q.get("answer") in q["options"]
                    ]
                    if not valid:
                        raise ValueError("The AI did not return valid quiz questions. Please try again.")
                    st.session_state["active_quiz"] = {
                        "topic": quiz_topic.strip(),
                        "questions": valid,
                        "provider": used
                    }
                    st.session_state.pop("quiz_submitted", None)
                    st.success(f"Created {len(valid)} questions using {used}.")
                except Exception as error:
                    st.error(f"Could not create quiz: {error}")

    quiz = st.session_state.get("active_quiz")
    if quiz:
        st.divider()
        st.subheader(f"Quiz: {quiz['topic']}")
        if not st.session_state.get("quiz_submitted", False):
            with st.form("answer_quiz_form"):
                answers = []
                for index, q in enumerate(quiz["questions"]):
                    st.markdown(f"**Q{index + 1}. {q['question']}**")
                    answers.append(
                        st.radio(
                            "Choose one answer",
                            q["options"],
                            index=None,
                            key=f"quiz_answer_{index}"
                        )
                    )
                submitted = st.form_submit_button("Submit answers")
            if submitted:
                score = sum(
                    answers[i] == q["answer"]
                    for i, q in enumerate(quiz["questions"])
                )
                st.session_state["quiz_answers"] = answers
                st.session_state["quiz_score"] = score
                st.session_state["quiz_submitted"] = True
                feature_db.save_quiz_result(
                    quiz["topic"], score, len(quiz["questions"])
                )
                st.rerun()
        else:
            score = st.session_state["quiz_score"]
            st.metric("Your score", f"{score}/{len(quiz['questions'])}",
                      f"{round(score / len(quiz['questions']) * 100)}%")
            for i, q in enumerate(quiz["questions"]):
                chosen = st.session_state["quiz_answers"][i]
                correct = chosen == q["answer"]
                st.markdown(f"**Q{i + 1}. {q['question']}**")
                st.write(f"Your answer: {chosen or 'Not answered'}")
                st.write(f"Correct answer: {q['answer']}")
                explanation = q.get("explanation", "Review the correct answer and try again.")
                if correct:
                    st.success(f"Correct! {explanation}")
                else:
                    st.error(f"Not quite. {explanation}")
            if st.button("Create another quiz"):
                st.session_state.pop("active_quiz", None)
                st.session_state.pop("quiz_submitted", None)
                st.rerun()


# ==================================================
# SMART FLASHCARDS
# ==================================================

elif page == "Smart Flashcards":

    from ai_engine import generate_ai_text
    import json

    st.title("🗂️ Smart Flashcards")
    st.write("Generate and save revision cards, then test your recall.")

    with st.form("flashcard_generate_form"):
        flash_topic = st.text_input("Topic", placeholder="Example: Database normalization")
        flash_count = st.selectbox("Number of cards", [5, 10], index=0)
        flash_provider = st.selectbox(
            "AI provider",
            ["Gemini", "Ollama (local)", "Automatic fallback (Ollama → Gemini)"]
        )
        make_cards = st.form_submit_button("Generate flashcards")

    if make_cards:
        if not flash_topic.strip():
            st.warning("Enter a topic.")
        else:
            prompt = f"""
Create {flash_count} useful study flashcards about {flash_topic}.
Return ONLY valid JSON in this exact format:
{{"cards":[{{"question":"Question","answer":"Concise answer"}}]}}
No markdown fences. Make answers accurate and concise.
"""
            with st.spinner("Generating flashcards..."):
                try:
                    response, used = generate_ai_text(prompt, flash_provider)
                    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", response.strip(), flags=re.I)
                    data = json.loads(cleaned)
                    cards = [
                        c for c in data.get("cards", [])
                        if c.get("question") and c.get("answer")
                    ]
                    if not cards:
                        raise ValueError("No valid flashcards were returned.")
                    feature_db.save_flashcards(flash_topic.strip(), cards)
                    st.success(f"Saved {len(cards)} flashcards using {used}.")
                except Exception as error:
                    st.error(f"Could not generate flashcards: {error}")

    st.divider()
    topics = feature_db.get_flashcard_topics()
    if topics:
        selected_flash_topic = st.selectbox("Choose a flashcard set", topics)
        cards = feature_db.get_flashcards(selected_flash_topic)
        if cards:
            if "flash_index" not in st.session_state:
                st.session_state["flash_index"] = 0
            st.session_state["flash_index"] %= len(cards)
            card = cards[st.session_state["flash_index"]]
            st.caption(f"Card {st.session_state['flash_index'] + 1} of {len(cards)}")
            with st.container(border=True):
                st.subheader(card["question"])
                if st.toggle("Reveal answer", key=f"reveal_{card['id']}"):
                    st.write(card["answer"])
            c1, c2, c3 = st.columns(3)
            if c1.button("⬅ Previous"):
                st.session_state["flash_index"] = (st.session_state["flash_index"] - 1) % len(cards)
                st.rerun()
            if c2.button("Next ➡"):
                st.session_state["flash_index"] = (st.session_state["flash_index"] + 1) % len(cards)
                st.rerun()
            if c3.button("Shuffle"):
                import random
                st.session_state["flash_index"] = random.randrange(len(cards))
                st.rerun()
    else:
        st.info("No flashcards saved yet. Generate your first set above.")


# ==================================================
# EXAM COUNTDOWN
# ==================================================

elif page == "Exam Countdown":

    st.title("📅 Exam Countdown")
    st.write("Save upcoming exams and see how much preparation time remains.")

    with st.form("add_exam_form"):
        exam_name = st.text_input("Exam name", placeholder="Example: Data Structures")
        exam_subject = st.text_input("Subject")
        exam_day = st.date_input("Exam date", min_value=date.today())
        add_exam = st.form_submit_button("Add exam")
    if add_exam:
        if exam_name.strip() and exam_subject.strip():
            feature_db.add_exam(exam_name.strip(), exam_subject.strip(), exam_day.isoformat())
            st.success("Exam saved.")
            st.rerun()
        else:
            st.error("Enter both exam name and subject.")

    st.divider()
    exams = feature_db.get_exams()
    if exams:
        for exam in exams:
            days_left = (date.fromisoformat(exam["exam_date"]) - date.today()).days
            with st.container(border=True):
                st.subheader(exam["name"])
                st.write(f"Subject: {exam['subject']}")
                st.metric("Days remaining", max(days_left, 0))
                if days_left == 0:
                    st.warning("Exam is today!")
                elif days_left < 0:
                    st.caption("This exam date has passed.")
                if st.button("Delete exam", key=f"delete_exam_{exam['id']}"):
                    feature_db.delete_exam(exam["id"])
                    st.rerun()
    else:
        st.info("No upcoming exams saved.")


# ==================================================
# WEEKLY ANALYTICS
# ==================================================

elif page == "Weekly Analytics":

    st.title("📈 Weekly Study Analytics")
    st.caption("Understand your study consistency and learning performance.")

    sessions = database.get_study_sessions()
    today = date.today()
    from datetime import timedelta
    week_start = today - timedelta(days=today.weekday())

    daily_totals = {}
    for offset in range(7):
        day = week_start + timedelta(days=offset)
        daily_totals[day.strftime("%a")] = sum(
            int(session["duration"])
            for session in sessions
            if str(session["study_date"])[:10] == day.isoformat()
        )

    total_week_minutes = sum(daily_totals.values())
    quiz_stats = feature_db.get_quiz_stats()

    st.markdown("### This week's overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Study time this week", f"{total_week_minutes // 60}h {total_week_minutes % 60}m")
    c2.metric("Quiz attempts", quiz_stats["attempts"])
    c3.metric("Average quiz score", f"{quiz_stats['average']}%")

    st.markdown("### 📅 Daily study activity")
    max_minutes = max(daily_totals.values()) if daily_totals else 0
    for day_name, minutes in daily_totals.items():
        left, right = st.columns([1, 5])
        left.markdown(f"**{day_name}**")
        with right:
            st.progress(minutes / max(1, max_minutes))
            st.caption(f"{minutes} minutes")

    st.markdown("### 📚 Study time by subject")
    subject_totals = {}
    for session in sessions:
        subject_name = session["subject"]
        subject_totals[subject_name] = subject_totals.get(subject_name, 0) + int(session["duration"])

    if subject_totals:
        max_subject = max(subject_totals.values())
        for subject_name, minutes in sorted(subject_totals.items(), key=lambda item: item[1], reverse=True):
            left, right = st.columns([2, 5])
            left.markdown(f"**{subject_name}**")
            with right:
                st.progress(minutes / max(1, max_subject))
                st.caption(f"{minutes} minutes")
    else:
        st.info("Record study sessions to see your subject-wise analytics.")

    st.caption("Analytics use your recorded study sessions and saved quiz attempts.")

elif page == "Achievements":

    st.title("🏆 Achievements")
    st.write("Celebrate your learning milestones and build consistent study habits.")

    tasks = database.get_tasks()
    sessions = database.get_study_sessions()
    completed_tasks = sum(bool(task["completed"]) for task in tasks)
    total_minutes = sum(int(session["duration"]) for session in sessions)
    quiz_stats = feature_db.get_quiz_stats()

    milestones = [
        ("first_task", "First Step", "Add your first study task.", len(tasks) >= 1),
        ("task_finisher", "Task Finisher", "Complete 5 study tasks.", completed_tasks >= 5),
        ("first_session", "Getting Started", "Record your first study session.", len(sessions) >= 1),
        ("study_5_hours", "Five-Hour Scholar", "Record 5 total study hours.", total_minutes >= 300),
        ("quiz_starter", "Quiz Explorer", "Complete your first AI quiz.", quiz_stats["attempts"] >= 1),
        ("quiz_master", "Quiz Champion", "Complete 5 AI quizzes.", quiz_stats["attempts"] >= 5),
    ]

    for code, title, description, earned in milestones:
        if earned:
            feature_db.unlock_achievement(code, title, description)

    earned_codes = {item["code"] for item in feature_db.get_achievements()}
    cols = st.columns(3)
    for index, (code, title, description, earned) in enumerate(milestones):
        with cols[index % 3]:
            with st.container(border=True):
                if code in earned_codes:
                    st.markdown("## 🏅")
                    st.markdown(f"**{title}**")
                    st.caption(description)
                    st.success("Unlocked")
                else:
                    st.markdown("## 🔒")
                    st.markdown(f"**{title}**")
                    st.caption(description)
                    st.info("Not unlocked yet")

    st.divider()
    points = completed_tasks * 10 + len(sessions) * 5 + quiz_stats["attempts"] * 10
    st.metric("Learning points", points)
    st.caption("Points are calculated from completed tasks, recorded study sessions and quiz attempts.")


# ==================================================
# FOCUS TIMER
# ==================================================

elif page == "Focus Timer":

    st.title("⏱️ Focus Studio")
    st.caption("Work in focused intervals, take refreshing breaks and build a consistent study habit.")

    setting1, setting2 = st.columns(2)
    with setting1:
        focus_minutes = st.selectbox(
            "🎯 Focus duration",
            [15, 25, 30, 45, 60],
            index=1,
            key="focus_duration"
        )
    with setting2:
        break_minutes = st.selectbox(
            "☕ Break duration",
            [5, 10, 15],
            index=0,
            key="break_duration"
        )

    timer_html = """
    <!DOCTYPE html>
    <html>
    <head>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { box-sizing: border-box; }
        body { margin: 0; padding: 8px; font-family: Arial, sans-serif; background: transparent; }
        .timer-card {
            max-width: 760px; margin: auto; padding: 30px 22px; text-align: center;
            border-radius: 22px; color: #fff;
            background: linear-gradient(145deg, #20234b, #343875);
            box-shadow: 0 12px 30px rgba(30,30,80,.18);
        }
        .tag { display: inline-block; padding: 7px 16px; border-radius: 30px;
            background: rgba(255,255,255,.13); color: #e3e2ff; font-size: 12px;
            font-weight: 700; letter-spacing: 1px; }
        .heading { margin: 18px 0 6px; font-size: 24px; font-weight: 800; }
        .subheading { color: #c5c8ed; font-size: 14px; }
        .clock { margin: 22px 0 16px; font-size: clamp(62px, 12vw, 94px);
            font-weight: 800; letter-spacing: 2px; font-variant-numeric: tabular-nums; }
        .track { max-width: 440px; height: 9px; margin: 0 auto 18px;
            border-radius: 20px; overflow: hidden; background: rgba(255,255,255,.17); }
        .fill { width: 100%; height: 100%; border-radius: 20px;
            background: linear-gradient(90deg, #a5a0ff, #d2cfff); transition: width .4s linear; }
        .message { min-height: 22px; margin: 12px 0 22px; color: #e0e1ff; font-size: 14px; }
        .buttons { display: flex; justify-content: center; flex-wrap: wrap; gap: 10px; }
        button { min-width: 112px; padding: 12px 20px; border: 0; border-radius: 10px;
            font-size: 14px; font-weight: 750; cursor: pointer; }
        button:hover { filter: brightness(1.08); transform: translateY(-1px); }
        .start { background: #8b83ff; color: #fff; }
        .pause { background: #fff; color: #292c60; }
        .reset { background: #454a82; color: #fff; border: 1px solid rgba(255,255,255,.2); }
        .stats { display: flex; justify-content: center; flex-wrap: wrap; gap: 32px; margin-top: 25px;
            color: #c5c8ed; font-size: 12px; }
        .stats strong { display: block; margin-top: 5px; color: #fff; font-size: 17px; }
        @media(max-width: 480px) { .timer-card { padding: 24px 12px; } button { min-width: 90px; padding: 11px 13px; } }
    </style>
    </head>
    <body>
      <div class="timer-card">
        <div class="tag" id="mode">FOCUS SESSION</div>
        <div class="heading">Make this session count.</div>
        <div class="subheading">One task at a time. Stay consistent.</div>
        <div class="clock" id="timer">__FOCUS__:00</div>
        <div class="track"><div class="fill" id="progress"></div></div>
        <div class="message" id="message">Ready when you are. Click Start to begin.</div>
        <div class="buttons">
          <button class="start" onclick="startTimer()">▶ Start</button>
          <button class="pause" onclick="pauseTimer()">Ⅱ Pause</button>
          <button class="reset" onclick="resetTimer()">↻ Reset</button>
        </div>
        <div class="stats">
          <div>FOCUS<strong id="focusLabel">__FOCUS__ min</strong></div>
          <div>BREAK<strong id="breakLabel">__BREAK__ min</strong></div>
          <div>COMPLETED<strong id="completedLabel">0</strong></div>
        </div>
      </div>
      <script>
        const focusSeconds = Number("__FOCUS__") * 60;
        const breakSeconds = Number("__BREAK__") * 60;
        let remaining = focusSeconds;
        let isBreak = false;
        let interval = null;
        let completedSessions = 0;

        function displayTime() {
          const minutes = Math.floor(remaining / 60);
          const seconds = remaining % 60;
          document.getElementById("timer").innerText =
            String(minutes).padStart(2, "0") + ":" + String(seconds).padStart(2, "0");
          const total = isBreak ? breakSeconds : focusSeconds;
          document.getElementById("progress").style.width =
            (total > 0 ? (remaining / total) * 100 : 0) + "%";
        }

        function startTimer() {
          if (interval !== null) return;
          document.getElementById("message").innerText = isBreak
            ? "Enjoy your break. Recharge!" : "Focus mode active. Keep going!";
          interval = setInterval(function() {
            if (remaining > 0) {
              remaining--;
              displayTime();
            } else {
              clearInterval(interval);
              interval = null;
              if (!isBreak) {
                completedSessions++;
                document.getElementById("completedLabel").innerText = completedSessions;
                isBreak = true;
                remaining = breakSeconds;
                document.getElementById("mode").innerText = "BREAK TIME";
                document.getElementById("message").innerText =
                  "Focus session complete! Start your break when ready.";
              } else {
                isBreak = false;
                remaining = focusSeconds;
                document.getElementById("mode").innerText = "FOCUS SESSION";
                document.getElementById("message").innerText =
                  "Break complete! Start another focus session when ready.";
              }
              displayTime();
            }
          }, 1000);
        }

        function pauseTimer() {
          if (interval !== null) {
            clearInterval(interval);
            interval = null;
            document.getElementById("message").innerText = "Timer paused. Resume whenever you're ready.";
          }
        }

        function resetTimer() {
          if (interval !== null) clearInterval(interval);
          interval = null;
          isBreak = false;
          remaining = focusSeconds;
          document.getElementById("mode").innerText = "FOCUS SESSION";
          document.getElementById("message").innerText = "Timer reset. Ready for a fresh start!";
          displayTime();
        }
        displayTime();
      </script>
    </body>
    </html>
    """

    timer_html = (
        timer_html
        .replace("__FOCUS__", str(int(focus_minutes)))
        .replace("__BREAK__", str(int(break_minutes)))
    )
    components.html(timer_html, height=490, scrolling=False)

    st.divider()
    st.markdown("### 💡 A simple focus routine")
    tip1, tip2, tip3 = st.columns(3)
    with tip1:
        with st.container(border=True):
            st.markdown("#### 🎯 Focus")
            st.caption("Choose one task and give it your full attention.")
    with tip2:
        with st.container(border=True):
            st.markdown("#### ☕ Recharge")
            st.caption("Stretch, drink water and rest your eyes.")
    with tip3:
        with st.container(border=True):
            st.markdown("#### 🏆 Repeat")
            st.caption("Return refreshed and continue making progress.")

    st.info(
        "The timer runs inside your browser. Its counter is temporary and is not saved automatically. "
        "Record completed study time in Daily Study Tracker to include it in your analytics."
    )


# ==================================================
# FOOTER
# ==================================================

st.sidebar.divider()
st.sidebar.caption("AI-Powered Personal Study Assistant")
st.sidebar.caption("Built with Python, Streamlit and SQLite")
