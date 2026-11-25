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

# Supabase Credentials (Streamlit Cloud Secrets)
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

# Load all 14 historical tasks exported from local PostgreSQL
historical_tasks_path = os.path.join(os.path.dirname(__file__), "local_tasks_export.json")
historical_tasks = []
if os.path.exists(historical_tasks_path):
    with open(historical_tasks_path, "r", encoding="utf-8") as f:
        historical_tasks = json.load(f)

hardcoded_catalog = [
    {"catalog_id": 1, "task_type": "Meeting", "task_name": "Requirement-Gathering Meeting", "task_description": "Meet stakeholders to collect network expansion requirements for new areas and societies."},
    {"catalog_id": 2, "task_type": "Meeting", "task_name": "Weekly Planning & GIS Meeting", "task_description": "Attend the weekly meeting to discuss and resolve planning and GIS issues, review pending items and agree on actions."},
    {"catalog_id": 3, "task_type": "Data Management", "task_name": "PON Port Data Management", "task_description": "Maintain PON port records and update the related GIS/database information."},
    {"catalog_id": 4, "task_type": "Data Management", "task_name": "As-Built Data Update", "task_description": "Update as-built records and drawings in the database."},
    {"catalog_id": 5, "task_type": "Data Management", "task_name": "GIS Data Integrity & QC", "task_description": "Find and fix data anomalies, wrong labels, missing attributes and other GIS inconsistencies."},
    {"catalog_id": 6, "task_type": "Design & Drawing", "task_name": "Splicing Plan Preparation", "task_description": "Prepare fiber splicing plans for new and existing deployments."},
    {"catalog_id": 7, "task_type": "Design & Drawing", "task_name": "Technical Drawing & Map Preparation", "task_description": "Prepare network maps, CLDs (Connection Layout Diagrams) and DLDs (Detailed Layout Diagrams)."},
    {"catalog_id": 8, "task_type": "GIS Update", "task_name": "Coverage KMZ Update", "task_description": "Update the coverage KMZ with each area status: In Coverage, In Progress or Out of Coverage."},
    {"catalog_id": 9, "task_type": "GIS Update", "task_name": "GIS Portal Coverage Map Update", "task_description": "Update and maintain coverage maps on the GIS Portal."},
    {"catalog_id": 10, "task_type": "GIS Update", "task_name": "Website Coverage Update", "task_description": "Keep coverage information on the company website accurate and current."},
    {"catalog_id": 11, "task_type": "GIS Update", "task_name": "Daily Customer Point Mapping", "task_description": "Plot and maintain the day's customer points on GIS."},
    {"catalog_id": 12, "task_type": "GIS Update", "task_name": "Parcel Preparation & DB Update", "task_description": "Prepare parcels for upcoming and underdeveloped areas and add them to the GIS database."},
    {"catalog_id": 13, "task_type": "New Planning", "task_name": "New Area Planning & BOQ", "task_description": "Plan new coverage areas and prepare their Bills of Quantities (BOQs)."},
    {"catalog_id": 14, "task_type": "New Planning", "task_name": "POP Finalization", "task_description": "Survey to finalize Point of Presence locations and prepare the BOQs and Capacity Planning."},
    {"catalog_id": 15, "task_type": "New Planning", "task_name": "Commercial Special Projects", "task_description": "Support special commercial requirements such as FTTT, bank sites, schools, hospitals etc."},
    {"catalog_id": 16, "task_type": "New Planning", "task_name": "Potential Area Data Preparation", "task_description": "Prepare HP data, KMZ files and planning information for areas targeted for expansion."},
    {"catalog_id": 17, "task_type": "Re-Planning", "task_name": "BOQ Review & Rework", "task_description": "Reassess previously planned areas and revise BOQs to the updated formats and requirements."},
    {"catalog_id": 18, "task_type": "Re-Planning", "task_name": "Network Re-Planning", "task_description": "Revise existing plans for updated SOPs, changed requirements and deployment models (aerial and UG)."},
    {"catalog_id": 19, "task_type": "Re-Planning", "task_name": "Ring Network Planning", "task_description": "Prepare ring plans for existing areas, including all DCs in the ring topology where technically feasible."},
    {"catalog_id": 20, "task_type": "Reporting", "task_name": "Network Element Data Preparation", "task_description": "Prepare inventory data (splitters, FATs, DCs, cable types, lengths) for PTA, management and FLL reporting."},
    {"catalog_id": 21, "task_type": "Reporting", "task_name": "Project Tracker Management", "task_description": "Maintain and update the planning project tracker with progress, pending items and status."},
    {"catalog_id": 22, "task_type": "Team Support", "task_name": "Operations Data Support", "task_description": "Provide the Operations team with exact locations, maps, network element details and custom data."},
    {"catalog_id": 23, "task_type": "Team Support", "task_name": "Cross-Functional Query Support", "task_description": "Answer planning and feasibility queries from Sales, Access, IP, Resellers, Commercial, Corporate Connectivity, DF and CIR Connectivity."},
    {"catalog_id": 24, "task_type": "Team Support", "task_name": "Third-Party LMP Feasibility", "task_description": "Assess third-party Last-Mile Provider feasibility, maintain records and process connectivity requests."},
    {"catalog_id": 25, "task_type": "Survey", "task_name": "As-Built Field Data Collection", "task_description": "Collect and verify field data needed for as-built documentation."},
    {"catalog_id": 26, "task_type": "Survey", "task_name": "Network Expansion Survey", "task_description": "Conduct field surveys to support daily network expansion and planning."},
    {"catalog_id": 27, "task_type": "Survey", "task_name": "MDU Survey & Planning", "task_description": "Survey Multi-Dwelling Units and prepare the corresponding network plans."},
    {"catalog_id": 28, "task_type": "Survey", "task_name": "Ops & Development Survey Support", "task_description": "Conduct surveys and give technical clarification to resolve field issues, planning discrepancies and deployment problems."},
    {"catalog_id": 29, "task_type": "Survey", "task_name": "ROW Survey", "task_description": "Conduct Right-of-Way surveys and provide technical information for ROW coordination and approvals."},
    {"catalog_id": 30, "task_type": "Survey", "task_name": "HP Survey & Verification", "task_description": "Verify Homes Passed counts in new and existing areas and update the Network Loading Sheet."}
]

# Supabase REST Bridge with Full Historical Tasks, File Support & Fallback
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

    var HISTORICAL_TASKS = {json.dumps(historical_tasks)};

    var LOCAL_MEMBERS = [
        {{ email: "fazal.admin@transworld.com", name: "Fazal ur Raheem", role: "Boss", region: "North", designation: "Admin & Operations Lead" }},
        {{ email: "hasaan.north@transworld.com", name: "Hasaan", role: "Member", region: "North", designation: "GIS Field Engineer" }},
        {{ email: "zain.north@transworld.com", name: "Zain", role: "Member", region: "North", designation: "GIS Field Engineer" }},
        {{ email: "annas.north@transworld.com", name: "Annas Bashir", role: "Member", region: "North", designation: "Senior GIS Surveyor" }},
        {{ email: "saboor.north@transworld.com", name: "Saboor Khan", role: "Member", region: "North", designation: "BOQ Estimator Lead" }}
    ];

    var loggedInUser = null;
    try {{
        var savedUser = sessionStorage.getItem('tw_logged_user');
        if (savedUser) loggedInUser = JSON.parse(savedUser);
    }} catch(e) {{}}

    function getMemberName(email) {{
        var e = (email || '').toLowerCase();
        var m = LOCAL_MEMBERS.find(function(x) {{ return x.email.toLowerCase() === e; }});
        return m ? m.name : email;
    }}

    function mapTask(t) {{
        var files = Array.isArray(t.task_files) ? t.task_files : (Array.isArray(t.files) ? t.files : []);
        var dl = (t.deadline || '').toString();
        return {{
            task_id: t.task_id,
            task_code: t.task_code,
            title: t.title,
            task_type: t.task_type,
            region: t.region || 'North',
            area_name: t.area_name || '',
            lat: t.latitude != null ? parseFloat(t.latitude) : (t.lat != null ? parseFloat(t.lat) : null),
            lng: t.longitude != null ? parseFloat(t.longitude) : (t.lng != null ? parseFloat(t.lng) : null),
            assigned_to: t.assigned_to,
            assignee_name: t.assignee_name || getMemberName(t.assigned_to),
            assigned_by: t.assigned_by || 'fazal.admin@transworld.com',
            deadline: t.deadline,
            deadline_str: t.deadline_str || dl.replace('T', ' ').slice(0, 16),
            priority: t.priority || 'Medium',
            status: t.status || 'Pending',
            description: t.description || '',
            submission_notes: t.submission_notes || '',
            report_filename: t.report_filename || '',
            boss_feedback: t.boss_feedback || '',
            submitted_at: t.submitted_at || null,
            reviewed_at: t.reviewed_at || null,
            assignee_seen_at: t.assignee_seen_at || null,
            file_count: files.length > 0 ? files.length : (t.file_count || 0),
            files: files
        }};
    }}

    function base64ToHex(b64) {{
        var raw = atob(b64);
        var hex = '';
        for (var i = 0; i < raw.length; i++) {{
            var h = raw.charCodeAt(i).toString(16);
            hex += (h.length === 2 ? h : '0' + h);
        }}
        return '\\\\x' + hex;
    }}

    function hexToUint8Array(hexStr) {{
        if (!hexStr) return new Uint8Array(0);
        if (hexStr.indexOf('\\\\x') === 0 || hexStr.indexOf('0x') === 0) {{
            hexStr = hexStr.slice(2);
        }}
        var bytes = new Uint8Array(hexStr.length / 2);
        for (var i = 0; i < bytes.length; i++) {{
            bytes[i] = parseInt(hexStr.substr(i * 2, 2), 16);
        }}
        return bytes;
    }}

    function fetchAllLiveTasks() {{
        return originalFetch(SB_URL + "/field_tasks?select=*,task_files(file_id,filename,file_type,size_bytes)&order=task_id.desc", {{ headers: SB_HEADERS }})
        .then(function(res) {{
            if (!res.ok) {{
                return originalFetch(SB_URL + "/field_tasks?select=*&order=task_id.desc", {{ headers: SB_HEADERS }})
                .then(function(res2) {{ return res2.ok ? res2.json() : []; }});
            }}
            return res.json();
        }})
        .then(function(supabaseTasks) {{
            var liveList = Array.isArray(supabaseTasks) ? supabaseTasks.map(mapTask) : [];
            var existingIds = new Set(liveList.map(function(x) {{ return x.task_id; }}));
            var existingCodes = new Set(liveList.map(function(x) {{ return x.task_code; }}));
            var merged = liveList.slice();
            HISTORICAL_TASKS.forEach(function(ht) {{
                if (!existingIds.has(ht.task_id) && !existingCodes.has(ht.task_code)) {{
                    merged.push(mapTask(ht));
                }}
            }});
            merged.sort(function(a, b) {{ return (b.task_id || 0) - (a.task_id || 0); }});
            return merged;
        }})
        .catch(function() {{
            return HISTORICAL_TASKS.map(mapTask);
        }});
    }}

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
            var pw = (body.password || '').trim();

            if (pw !== 'transworld123' && pw !== 'admin') {{
                return Promise.resolve(new Response(JSON.stringify({{ error: "Invalid username or password" }}), {{
                    status: 401,
                    headers: {{ 'Content-Type': 'application/json' }}
                }}));
            }}

            var found = LOCAL_MEMBERS.find(function(m) {{ return m.email.toLowerCase() === email; }});
            if (found) {{
                loggedInUser = found;
                try {{ sessionStorage.setItem('tw_logged_user', JSON.stringify(found)); }} catch(e) {{}}
                return Promise.resolve(new Response(JSON.stringify({{ status: 'ok', user: found }}), {{
                    status: 200,
                    headers: {{ 'Content-Type': 'application/json' }}
                }}));
            }}

            return originalFetch(SB_URL + "/team_members?email=ilike." + encodeURIComponent(email) + "&select=*", {{
                headers: SB_HEADERS
            }})
            .then(function(res) {{ return res.json(); }})
            .then(function(users) {{
                if (Array.isArray(users) && users.length > 0) {{
                    var uObj = users[0];
                    var userData = {{ email: uObj.email, name: uObj.name, role: uObj.role, region: uObj.region, designation: uObj.designation || '' }};
                    loggedInUser = userData;
                    try {{ sessionStorage.setItem('tw_logged_user', JSON.stringify(userData)); }} catch(e) {{}}
                    return new Response(JSON.stringify({{
                        status: 'ok',
                        user: userData
                    }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
                }}
                return new Response(JSON.stringify({{ error: "User not found in system" }}), {{ status: 401, headers: {{ 'Content-Type': 'application/json' }} }});
            }})
            .catch(function(err) {{
                return new Response(JSON.stringify({{ error: "Database error: " + err.message }}), {{ status: 500, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 2. LOGOUT
        if (u.indexOf('/api/logout') !== -1) {{
            loggedInUser = null;
            try {{ sessionStorage.removeItem('tw_logged_user'); }} catch(e) {{}}
            return Promise.resolve(new Response(JSON.stringify({{ status: 'logged_out' }}), {{ status: 200 }}));
        }}

        // 3. TASK CATALOG (Supabase + Hardcoded fallback)
        if (u.indexOf('/api/task-catalog') !== -1) {{
            var HARDCODED_CATALOG = {json.dumps(hardcoded_catalog)};
            return originalFetch(SB_URL + "/task_catalog?select=*&order=catalog_id.asc", {{ headers: SB_HEADERS }})
            .then(function(res) {{ return res.json(); }})
            .then(function(catalog) {{
                var result = (Array.isArray(catalog) && catalog.length > 0) ? catalog : HARDCODED_CATALOG;
                return new Response(JSON.stringify(result), {{ status: 200, headers: {{ "Content-Type": "application/json" }} }});
            }})
            .catch(function() {{
                return new Response(JSON.stringify(HARDCODED_CATALOG), {{ status: 200, headers: {{ "Content-Type": "application/json" }} }});
            }});
        }}

        // 4. TEAMS
        if (u.indexOf('/api/teams') !== -1) {{
            return originalFetch(SB_URL + "/team_members?select=*&order=name.asc", {{ headers: SB_HEADERS }})
            .then(function(res) {{ return res.json(); }})
            .then(function(list) {{
                var teams = (Array.isArray(list) && list.length > 0) ? list : LOCAL_MEMBERS;
                return new Response(JSON.stringify(teams), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }})
            .catch(function() {{
                return new Response(JSON.stringify(LOCAL_MEMBERS), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 5. GET TASK FILES LIST
        if (u.indexOf('/api/tasks/files') !== -1 && method === 'GET') {{
            var taskIdMatch = u.match(/task_id=(\\d+)/);
            var tid = taskIdMatch ? taskIdMatch[1] : '';
            if (!tid) return Promise.resolve(new Response('[]', {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }}));
            return originalFetch(SB_URL + "/task_files?task_id=eq." + tid + "&select=file_id,task_id,filename,file_type,size_bytes,uploaded_by,uploaded_at", {{ headers: SB_HEADERS }})
            .then(function(res) {{ return res.ok ? res.json() : []; }})
            .then(function(rows) {{
                return new Response(JSON.stringify(Array.isArray(rows) ? rows : []), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }})
            .catch(function() {{
                return new Response('[]', {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 5b. DOWNLOAD SINGLE TASK FILE
        if (u.indexOf('/api/tasks/file') !== -1 && method === 'GET') {{
            var fileIdMatch = u.match(/file_id=(\\d+)/);
            var fid = fileIdMatch ? fileIdMatch[1] : '';
            if (!fid) return Promise.resolve(new Response('File not found', {{ status: 404 }}));
            return originalFetch(SB_URL + "/task_files?file_id=eq." + fid + "&select=filename,file_type,content", {{ headers: SB_HEADERS }})
            .then(function(res) {{ return res.json(); }})
            .then(function(rows) {{
                if (!Array.isArray(rows) || rows.length === 0) {{
                    return new Response('File not found', {{ status: 404 }});
                }}
                var f = rows[0];
                var bytes = hexToUint8Array(f.content);
                return new Response(bytes, {{
                    status: 200,
                    headers: {{
                        'Content-Type': 'application/octet-stream',
                        'Content-Disposition': 'attachment; filename="' + (f.filename || 'attachment') + '"'
                    }}
                }});
            }});
        }}

        // 5c. NOTIFICATIONS
        if (u.indexOf('/api/notifications') !== -1 && method === 'GET') {{
            return fetchAllLiveTasks().then(function(tasks) {{
                if (!loggedInUser || loggedInUser.role === 'Boss') {{
                    return new Response(JSON.stringify({{ unseen_count: 0, tasks: [] }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
                }}
                var mine = tasks.filter(function(t) {{
                    return (t.assigned_to || '').toLowerCase() === loggedInUser.email.toLowerCase() && !t.assignee_seen_at;
                }});
                return new Response(JSON.stringify({{ unseen_count: mine.length, tasks: mine }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 5d. MARK SEEN
        if (u.indexOf('/api/tasks/mark-seen') !== -1 && method === 'POST') {{
            var p = JSON.parse(opts.body || '{{}}');
            return originalFetch(SB_URL + "/field_tasks?task_id=eq." + p.task_id, {{
                method: "PATCH",
                headers: SB_HEADERS,
                body: JSON.stringify({{ assignee_seen_at: new Date().toISOString() }})
            }})
            .then(function() {{
                return new Response(JSON.stringify({{ status: 'ok' }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }})
            .catch(function() {{
                return new Response(JSON.stringify({{ status: 'ok' }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 5e. GET TASKS (Merge Supabase live tasks + Historical Tasks, filter for Member)
        if (u.indexOf('/api/tasks') !== -1 && method === 'GET') {{
            return fetchAllLiveTasks().then(function(merged) {{
                if (loggedInUser && loggedInUser.role !== 'Boss') {{
                    var myEmail = loggedInUser.email.toLowerCase();
                    merged = merged.filter(function(t) {{
                        return (t.assigned_to || '').toLowerCase() === myEmail;
                    }});
                }}
                return new Response(JSON.stringify(merged), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 6. ANNUAL AUDIT REPORT API
        if (u.indexOf('/api/reports/annual') !== -1 && method === 'GET') {{
            return fetchAllLiveTasks().then(function(tasks) {{
                var total = tasks.length;
                var completed = tasks.filter(function(x) {{ return x.status === 'Accepted'; }}).length;
                var pending = total - completed;
                var rate = total > 0 ? ((completed / total) * 100).toFixed(1) : "0.0";

                var report = {{
                    year: 2026,
                    total_tasks: total,
                    completed_tasks: completed,
                    pending_tasks: pending,
                    completion_rate_pct: rate,
                    member_stats: LOCAL_MEMBERS.map(function(m) {{
                        var mTasks = tasks.filter(function(t) {{ return (t.assigned_to || '').toLowerCase() === m.email.toLowerCase(); }});
                        var mComp = mTasks.filter(function(t) {{ return t.status === 'Accepted'; }}).length;
                        return {{
                            name: m.name,
                            email: m.email,
                            role: m.role,
                            region: m.region,
                            designation: m.designation,
                            total_assigned: mTasks.length,
                            completed_tasks: mComp,
                            pending_tasks: mTasks.filter(function(t) {{ return t.status === 'Pending'; }}).length,
                            in_progress_tasks: mTasks.filter(function(t) {{ return t.status === 'In Progress'; }}).length,
                            completion_rate_pct: mTasks.length > 0 ? ((mComp / mTasks.length) * 100).toFixed(1) : "0.0"
                        }};
                    }}),
                    tasks: tasks
                }};

                return new Response(JSON.stringify(report), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 7. CREATE TASK + SAVE KML/KMZ ATTACHMENTS TO task_files
        if (u.indexOf('/api/tasks/create') !== -1 && method === 'POST') {{
            var payload = JSON.parse(opts.body || '{{}}');
            var taskData = {{
                task_code: "TSK-NOR-" + Math.floor(1000 + Math.random() * 9000),
                title: payload.title,
                task_type: payload.task_type,
                region: payload.region || 'North',
                area_name: payload.area_name || '',
                assigned_to: payload.assigned_to,
                assigned_by: (loggedInUser && loggedInUser.email) || 'fazal.admin@transworld.com',
                deadline: payload.deadline,
                priority: payload.priority || 'High',
                status: 'Pending',
                description: payload.description || ''
            }};

            return originalFetch(SB_URL + "/field_tasks", {{
                method: "POST",
                headers: SB_HEADERS,
                body: JSON.stringify(taskData)
            }})
            .then(function(res) {{
                return res.json().then(function(data) {{ return {{ ok: res.ok, status: res.status, data: data }}; }});
            }})
            .then(function(result) {{
                if (!result.ok || !Array.isArray(result.data) || result.data.length === 0) {{
                    var errMsg = (result.data && (result.data.message || result.data.details || result.data.hint)) || ("Supabase insert failed (HTTP " + result.status + ")");
                    return new Response(JSON.stringify({{ error: errMsg }}), {{ status: 400, headers: {{ 'Content-Type': 'application/json' }} }});
                }}
                var createdTask = result.data[0];
                var files = Array.isArray(payload.files) ? payload.files : [];
                if (files.length === 0) {{
                    return new Response(JSON.stringify({{ status: 'created', task: mapTask(createdTask) }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
                }}
                var filePromises = files.map(function(f) {{
                    var ext = (f.filename || '').split('.').pop().toLowerCase() || 'bin';
                    var fileRow = {{
                        task_id: createdTask.task_id,
                        filename: f.filename,
                        file_type: ext,
                        size_bytes: f.size_bytes || f.size || 0,
                        content: f.content_base64 ? base64ToHex(f.content_base64) : null,
                        uploaded_by: (loggedInUser && loggedInUser.email) || 'fazal.admin@transworld.com'
                    }};
                    return originalFetch(SB_URL + "/task_files", {{
                        method: "POST",
                        headers: SB_HEADERS,
                        body: JSON.stringify(fileRow)
                    }}).then(function(r) {{ return r.ok ? r.json() : null; }}).catch(function() {{ return null; }});
                }});
                return Promise.all(filePromises).then(function() {{
                    return new Response(JSON.stringify({{ status: 'created', task: mapTask(createdTask) }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
                }});
            }})
            .catch(function(err) {{
                return new Response(JSON.stringify({{ error: err.message || 'Network error' }}), {{ status: 500, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 8. UPDATE TASK STATUS
        if (u.indexOf('/api/tasks/update-status') !== -1 && method === 'POST') {{
            var payload = JSON.parse(opts.body || '{{}}');
            var patchBody = {{ status: payload.status }};
            if (payload.submission_notes !== undefined || payload.notes !== undefined) {{
                patchBody.submission_notes = payload.submission_notes || payload.notes || '';
            }}
            if (payload.report_filename !== undefined) {{
                patchBody.report_filename = payload.report_filename;
            }}
            if (payload.status === 'Submitted for Review') {{
                patchBody.submitted_at = new Date().toISOString();
            }}
            return originalFetch(SB_URL + "/field_tasks?task_id=eq." + payload.task_id, {{
                method: "PATCH",
                headers: SB_HEADERS,
                body: JSON.stringify(patchBody)
            }})
            .then(function(res) {{ return res.json(); }})
            .then(function() {{
                return new Response(JSON.stringify({{ status: 'updated' }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
            }});
        }}

        // 9. REVIEW TASK (Admin Accept / Reject)
        if (u.indexOf('/api/tasks/review') !== -1 && method === 'POST') {{
            var payload = JSON.parse(opts.body || '{{}}');
            return originalFetch(SB_URL + "/field_tasks?task_id=eq." + payload.task_id, {{
                method: "PATCH",
                headers: SB_HEADERS,
                body: JSON.stringify({{
                    status: payload.decision || payload.status,
                    boss_feedback: payload.boss_feedback || payload.feedback || '',
                    reviewed_at: new Date().toISOString()
                }})
            }})
            .then(function(res) {{ return res.json(); }})
            .then(function() {{
                return new Response(JSON.stringify({{ status: 'reviewed' }}), {{ status: 200, headers: {{ 'Content-Type': 'application/json' }} }});
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
