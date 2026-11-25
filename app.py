import streamlit as st
import streamlit.components.v1 as components
import os
import json

st.set_page_config(
    page_title="Transworld Task Portal",
    page_icon="🗺️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Streamlit Top Header & Footer Hide
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        .block-container { padding: 0rem !important; margin: 0rem !important; max-width: 100% !important; }
        iframe { position: fixed; top: 0; left: 0; width: 100vw !important; height: 100vh !important; border: none; margin: 0; padding: 0; overflow: hidden; z-index: 999999; }
    </style>
""", unsafe_allow_html=True)

# Supabase Credentials (Streamlit Cloud Secrets se load honge)
SUPABASE_URL = str(st.secrets.get("SUPABASE_URL", "")).strip().rstrip("/")
SUPABASE_KEY = str(st.secrets.get("SUPABASE_KEY", "")).strip()

if not SUPABASE_URL or not SUPABASE_KEY:
    st.error("Missing SUPABASE_URL or SUPABASE_KEY in Streamlit Secrets.")
    st.stop()

html_file = os.path.join(os.path.dirname(__file__), "index.html")
html_content = ""
if os.path.exists(html_file):
    with open(html_file, "r", encoding="utf-8") as f:
        html_content = f.read()

# Supabase REST Bridge
supabase_bridge = f"""
<script>
(function() {{
    var SB_URL = {json.dumps(SUPABASE_URL)} + "/rest/v1";
    var SB_KEY = {json.dumps(SUPABASE_KEY)};
    var SB_HEADERS = {{
        "apikey": SB_KEY,
        "Authorization": "Bearer " + SB_KEY,
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }};

    var originalFetch = window.fetch;
    window.fetch = function(url, options) {{
        var u = typeof url === 'string' ? url : (url && url.url ? url.url : '');
        var opts = options || {{}};
        var method = (opts.method || 'GET').toUpperCase();

        // 1. LOGIN API
        if (u.indexOf('/api/login') !== -1) {{
            var body = {{}};
            try {{ if (opts.body) body = JSON.parse(opts.body); }} catch(e) {{}}
            var email = (body.email || '').trim().toLowerCase();
            var pw = body.password || '';

            return originalFetch(SB_URL + "/team_members?email=ilike." + encodeURIComponent(email) + "&select=*", {{
                headers: SB_HEADERS
            }})
            .then(function(res) {{ return res.json(); }})
            .then(function(users) {{
                if (Array.isArray(users) && users.length > 0) {{
                    var user = users[0];
                    if (pw === 'transworld123' || pw === 'admin') {{
                        return new Response(JSON.stringify({{
                            status: 'ok',
                            user: {{ email: user.email, name: user.name, role: user.role, region: user.region, designation: user.designation || '' }}
                        }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
                    }}
                }}
                return new Response(JSON.stringify({{ error: "Invalid username or password" }}), {{ status: 401, headers: {{ 'Content-Type': 'application/json' }} }});
            }})
            .catch(function(err) {{
                console.error("Login bridge error:", err);
                return new Response(JSON.stringify({{ error: "Network error while connecting to database" }}), {{ status: 500, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 2. LOGOUT
        if (u.indexOf('/api/logout') !== -1) {{
            return Promise.resolve(new Response(JSON.stringify({{ status: 'logged_out' }}), {{ status: 200 }}));
        }}

        // 3. TASK CATALOG
        if (u.indexOf('/api/task-catalog') !== -1) {{
            return originalFetch(SB_URL + "/task_catalog?select=*&order=catalog_id.asc", {{ headers: SB_HEADERS }});
        }}

        // 4. TEAMS
        if (u.indexOf('/api/teams') !== -1) {{
            return originalFetch(SB_URL + "/team_members?select=*&order=name.asc", {{ headers: SB_HEADERS }});
        }}

        // 5. GET TASKS
        if (u.indexOf('/api/tasks') !== -1 && method === 'GET') {{
            return originalFetch(SB_URL + "/field_tasks?select=*,task_files(file_id,filename,file_type,size_bytes)&order=task_id.desc", {{ headers: SB_HEADERS }})
            .then(function(res) {{ return res.json(); }})
            .then(function(tasks) {{
                var mapped = (Array.isArray(tasks) ? tasks : []).map(function(t) {{
                    t.file_count = (t.task_files || []).length;
                    t.files = t.task_files || [];
                    return t;
                }});
                return new Response(JSON.stringify(mapped), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 6. CREATE TASK
        if (u.indexOf('/api/tasks/create') !== -1 && method === 'POST') {{
            var payload = JSON.parse(opts.body || '{{}}');
            var taskData = {{
                task_code: "TSK-NOR-" + Math.floor(1000 + Math.random() * 9000),
                title: payload.title,
                task_type: payload.task_type,
                region: payload.region || 'North',
                area_name: payload.area_name || '',
                assigned_to: payload.assigned_to,
                assigned_by: 'fazal.admin@transworld.com',
                deadline: payload.deadline,
                priority: payload.priority,
                status: 'Pending',
                description: payload.description
            }};

            return originalFetch(SB_URL + "/field_tasks", {{
                method: "POST",
                headers: SB_HEADERS,
                body: JSON.stringify(taskData)
            }})
            .then(function(res) {{ return res.json(); }})
            .then(function(created) {{
                return new Response(JSON.stringify({{ status: 'created', task: created[0] }}), {{ status: 200 }});
            }});
        }}

        return originalFetch(url, options);
    }};
}})();
</script>
"""

# HTML mein bridge inject karna
if html_content:
    injected_html = html_content.replace("<head>", "<head>\n" + supabase_bridge, 1)
    components.html(injected_html, height=1000, scrolling=True)
else:
    st.error("index.html not found.")
