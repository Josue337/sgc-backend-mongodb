import React, { useState, useEffect } from 'react';

const API_BASE_URL = 'https://yummy-readers-relate.loca.lt';

// Helper to decode JWT
const parseJwt = (token) => {
  try {
    return JSON.parse(atob(token.split('.')[1]));
  } catch (e) {
    return null;
  }
};

function App() {
  // Auth state
  const [token, setToken] = useState(localStorage.getItem('token') || '');
  const [user, setUser] = useState(null);
  const [authMode, setAuthMode] = useState('login'); // 'login' or 'register'
  
  // Auth Form State
  const [authError, setAuthError] = useState('');
  const [authSuccess, setAuthSuccess] = useState('');
  const [loginEmail, setLoginEmail] = useState('');
  const [loginPass, setLoginPass] = useState('');
  
  const [regId, setRegId] = useState('');
  const [regName, setRegName] = useState('');
  const [regDoc, setRegDoc] = useState('');
  const [regEmail, setRegEmail] = useState('');
  const [regRol, setRegRol] = useState('1'); // Standard role default
  const [regPass, setRegPass] = useState('');

  // Dashboard Data State
  const [cases, setCases] = useState([]);
  const [categories, setCategories] = useState([]);
  const [states, setStates] = useState([]);
  const [auditLogs, setAuditLogs] = useState([]);
  const [dashboardError, setDashboardError] = useState('');
  const [dashboardSuccess, setDashboardSuccess] = useState('');
  const [deleteConfirmId, setDeleteConfirmId] = useState(null);

  // Case Form State (Create / Edit)
  const [isEditing, setIsEditing] = useState(false);
  const [caseId, setCaseId] = useState('');
  const [caseTitle, setCaseTitle] = useState('');
  const [caseDesc, setCaseDesc] = useState('');
  const [casePriority, setCasePriority] = useState('Media');
  const [caseCategory, setCaseCategory] = useState('');
  const [caseState, setCaseState] = useState('');
  const [caseResponsable, setCaseResponsable] = useState('');

  // Decode user on startup/token change
  useEffect(() => {
    if (token) {
      const decoded = parseJwt(token);
      if (decoded) {
        setUser({
          id_usuario: decoded.sub,
          correo: decoded.correo,
          nombre: localStorage.getItem('user_name') || 'Usuario'
        });
      } else {
        handleLogout();
      }
    } else {
      setUser(null);
    }
  }, [token]);

  // Fetch all dashboard data when logged in
  useEffect(() => {
    if (token) {
      fetchDashboardData();
    }
  }, [token]);

  const fetchDashboardData = async () => {
    try {
      setDashboardError('');
      // Fetch cases
      const casesRes = await fetch(`${API_BASE_URL}/casos/`);
      if (casesRes.ok) {
        const casesData = await casesRes.json();
        setCases(casesData);
      }

      // Fetch master categories
      const catRes = await fetch(`${API_BASE_URL}/maestros/categorias`);
      if (catRes.ok) {
        const catData = await catRes.json();
        setCategories(catData);
        if (catData.length > 0 && !caseCategory) {
          setCaseCategory(catData[0].id_categoria.toString());
        }
      }

      // Fetch master states
      const stateRes = await fetch(`${API_BASE_URL}/maestros/estados`);
      if (stateRes.ok) {
        const stateData = await stateRes.json();
        setStates(stateData);
        if (stateData.length > 0 && !caseState) {
          setCaseState(stateData[0].id_estado.toString());
        }
      }

      // Fetch audit logs
      const auditRes = await fetch(`${API_BASE_URL}/casos/audit/logs`);
      if (auditRes.ok) {
        const auditData = await auditRes.json();
        setAuditLogs(auditData);
      }
    } catch (err) {
      setDashboardError('Error al sincronizar datos con el servidor.');
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('user_name');
    setToken('');
    setUser(null);
  };

  const handleLogin = async (e) => {
    e.preventDefault();
    setAuthError('');
    setAuthSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/auth/login`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          correo_electronico: loginEmail,
          contrasena: loginPass
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Error en el inicio de sesión.');
      }

      localStorage.setItem('token', data.access_token);
      // Intenta guardar un nombre aproximado o predeterminado para la UI
      localStorage.setItem('user_name', loginEmail.split('@')[0]);
      setToken(data.access_token);
      setAuthSuccess('¡Sesión iniciada con éxito!');
    } catch (err) {
      setAuthError(err.message);
    }
  };

  const handleRegister = async (e) => {
    e.preventDefault();
    setAuthError('');
    setAuthSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/auth/register`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          id_usuario: parseInt(regId),
          nombre: regName,
          documento: regDoc,
          correo_electronico: regEmail,
          id_rol: parseInt(regRol),
          contrasena: regPass
        })
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Error al registrar el usuario.');
      }

      setAuthSuccess('Usuario registrado con éxito. ¡Ya puedes iniciar sesión!');
      setAuthMode('login');
      setLoginEmail(regEmail);
      setLoginPass('');
    } catch (err) {
      setAuthError(err.message);
    }
  };

  const handleCreateOrUpdateCase = async (e) => {
    e.preventDefault();
    setDashboardError('');
    setDashboardSuccess('');

    if (!caseId || !caseTitle || !caseDesc) {
      setDashboardError('Por favor completa los campos requeridos.');
      return;
    }

    try {
      if (isEditing) {
        // UPDATE CASE (PUT)
        const response = await fetch(`${API_BASE_URL}/casos/${parseInt(caseId)}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
          },
          body: JSON.stringify({
            titulo_caso: caseTitle,
            descripcion: caseDesc,
            prioridad: casePriority,
            id_categoria: parseInt(caseCategory),
            id_estado: parseInt(caseState),
            id_responsable_asignado: caseResponsable ? parseInt(caseResponsable) : null
          })
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Error al actualizar el caso.');
        }

        setDashboardSuccess(`Caso ${caseId} actualizado con éxito y auditado.`);
        clearCaseForm();
      } else {
        // CREATE CASE (POST)
        const response = await fetch(`${API_BASE_URL}/casos/`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            id_caso: parseInt(caseId),
            titulo_caso: caseTitle,
            descripcion: caseDesc,
            prioridad: casePriority,
            id_categoria: parseInt(caseCategory),
            id_estado: parseInt(caseState),
            id_usuario_creador: parseInt(user.id_usuario),
            id_responsable_asignado: caseResponsable ? parseInt(caseResponsable) : null
          })
        });

        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.detail || 'Error al registrar el caso.');
        }

        setDashboardSuccess(`Caso ${data.id_caso} creado con éxito.`);
        clearCaseForm();
      }

      fetchDashboardData();
    } catch (err) {
      setDashboardError(err.message);
    }
  };

  const handleEditClick = (caso) => {
    setIsEditing(true);
    setCaseId(caso.id_caso.toString());
    setCaseTitle(caso.titulo_caso);
    setCaseDesc(caso.descripcion);
    setCasePriority(caso.prioridad);
    setCaseCategory(caso.id_categoria.toString());
    setCaseState(caso.id_estado.toString());
    setCaseResponsable(caso.id_responsable_asignado ? caso.id_responsable_asignado.toString() : '');
    setDashboardError('');
    setDashboardSuccess('');
  };

  const handleDeleteClick = async (id_caso) => {
    setDashboardError('');
    setDashboardSuccess('');

    try {
      const response = await fetch(`${API_BASE_URL}/casos/${id_caso}`, {
        method: 'DELETE'
      });

      const data = await response.json();
      if (!response.ok) {
        throw new Error(data.detail || 'Error al desactivar el caso.');
      }

      setDashboardSuccess(data.message || `Caso ${id_caso} desactivado correctamente.`);
      setDeleteConfirmId(null);
      fetchDashboardData();
    } catch (err) {
      setDashboardError(err.message);
    }
  };

  const clearCaseForm = () => {
    setIsEditing(false);
    setCaseId('');
    setCaseTitle('');
    setCaseDesc('');
    setCasePriority('Media');
    if (categories.length > 0) setCaseCategory(categories[0].id_categoria.toString());
    if (states.length > 0) setCaseState(states[0].id_estado.toString());
    setCaseResponsable('');
  };

  // Helper to resolve name from list IDs
  const getCategoryName = (id) => {
    const cat = categories.find(c => c.id_categoria === id);
    return cat ? cat.nombre_categoria : `Cat ${id}`;
  };

  const getStateName = (id) => {
    const st = states.find(s => s.id_estado === id);
    return st ? st.nombre_estado : `Estado ${id}`;
  };

  // Format Date ISO
  const formatDate = (isoString) => {
    if (!isoString) return '';
    const date = new Date(isoString);
    return date.toLocaleString('es-ES', {
      day: '2-digit',
      month: '2-digit',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  // ----------------------------------------------------
  // RENDER AUTH SCREEN
  // ----------------------------------------------------
  if (!token) {
    return (
      <div className="container auth-wrapper">
        <div className="glass-panel auth-card">
          <div className="auth-header">
            <h1 className="brand-logo" style={{ fontSize: '2.5rem', marginBottom: '0.5rem' }}>SGC API</h1>
            <p className="auth-subtitle">Gestión y Seguimiento de Casos (NoSQL)</p>
          </div>

          <div className="tabs" style={{ justifyContent: 'center' }}>
            <button 
              className={`tab ${authMode === 'login' ? 'active' : ''}`} 
              onClick={() => { setAuthMode('login'); setAuthError(''); setAuthSuccess(''); }}
            >
              Iniciar Sesión
            </button>
            <button 
              className={`tab ${authMode === 'register' ? 'active' : ''}`} 
              onClick={() => { setAuthMode('register'); setAuthError(''); setAuthSuccess(''); }}
            >
              Registrarse
            </button>
          </div>

          {authError && <div className="alert alert-danger">{authError}</div>}
          {authSuccess && <div className="alert alert-success">{authSuccess}</div>}

          {authMode === 'login' ? (
            <form onSubmit={handleLogin} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div className="form-group">
                <label className="form-label">Correo Electrónico</label>
                <input 
                  type="email" 
                  className="form-control" 
                  value={loginEmail} 
                  onChange={(e) => setLoginEmail(e.target.value)} 
                  placeholder="ejemplo@correo.com"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Contraseña</label>
                <input 
                  type="password" 
                  className="form-control" 
                  value={loginPass} 
                  onChange={(e) => setLoginPass(e.target.value)} 
                  placeholder="••••••••"
                  required
                />
              </div>

              <button type="submit" className="btn btn-primary" style={{ marginTop: '0.5rem' }}>
                Entrar al Sistema
              </button>
            </form>
          ) : (
            <form onSubmit={handleRegister} style={{ display: 'flex', flexDirection: 'column', gap: '0.8rem' }}>
              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">ID Usuario (Numérico)</label>
                  <input 
                    type="number" 
                    className="form-control" 
                    value={regId} 
                    onChange={(e) => setRegId(e.target.value)} 
                    placeholder="101"
                    required
                  />
                </div>
                <div className="form-group">
                  <label className="form-label">Documento</label>
                  <input 
                    type="text" 
                    className="form-control" 
                    value={regDoc} 
                    onChange={(e) => setRegDoc(e.target.value)} 
                    placeholder="1005234..."
                    required
                  />
                </div>
              </div>

              <div className="form-group">
                <label className="form-label">Nombre Completo</label>
                <input 
                  type="text" 
                  className="form-control" 
                  value={regName} 
                  onChange={(e) => setRegName(e.target.value)} 
                  placeholder="Carlos Pérez"
                  required
                />
              </div>

              <div className="form-group">
                <label className="form-label">Correo Electrónico</label>
                <input 
                  type="email" 
                  className="form-control" 
                  value={regEmail} 
                  onChange={(e) => setRegEmail(e.target.value)} 
                  placeholder="carlos@correo.com"
                  required
                />
              </div>

              <div className="form-row">
                <div className="form-group">
                  <label className="form-label">Rol (ID)</label>
                  <select 
                    className="form-control" 
                    value={regRol} 
                    onChange={(e) => setRegRol(e.target.value)}
                  >
                    <option value="1">Administrador (1)</option>
                    <option value="2">Soporte Técnico (2)</option>
                    <option value="3">Usuario Final (3)</option>
                  </select>
                </div>
                <div className="form-group">
                  <label className="form-label">Contraseña</label>
                  <input 
                    type="password" 
                    className="form-control" 
                    value={regPass} 
                    onChange={(e) => setRegPass(e.target.value)} 
                    placeholder="Mín. 6 caracteres"
                    required
                  />
                </div>
              </div>

              <button type="submit" className="btn btn-primary" style={{ marginTop: '0.5rem' }}>
                Registrar Cuenta
              </button>
            </form>
          )}
        </div>
      </div>
    );
  }

  // ----------------------------------------------------
  // RENDER DASHBOARD
  // ----------------------------------------------------
  return (
    <div className="container">
      {/* Header Banner */}
      <header className="glass-panel app-header">
        <div className="brand">
          <span className="brand-logo">SGC Dashboard</span>
        </div>
        <div className="user-badge">
          <div>
            <div className="user-name">{user?.nombre}</div>
            <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>{user?.correo}</div>
          </div>
          <span className="user-role">ID: {user?.id_usuario}</span>
          <button className="btn btn-secondary btn-sm" onClick={handleLogout}>
            Salir
          </button>
        </div>
      </header>

      {dashboardError && <div className="alert alert-danger">{dashboardError}</div>}
      {dashboardSuccess && <div className="alert alert-success">{dashboardSuccess}</div>}

      <div className="dashboard-grid">
        {/* Left Side: Cases List Table */}
        <section className="glass-panel" style={{ padding: '1.75rem' }}>
          <div className="section-title">
            <span>Listado de Casos Activos</span>
            <button className="btn btn-secondary btn-sm" onClick={fetchDashboardData}>
              🔄 Recargar
            </button>
          </div>

          {cases.length === 0 ? (
            <div className="empty-state">
              <div className="empty-state-icon">📂</div>
              <p>No se encontraron casos activos creados en la base de datos.</p>
              <p style={{ fontSize: '0.85rem', marginTop: '0.5rem', color: 'var(--text-muted)' }}>
                Usa el formulario de la derecha para registrar el primero.
              </p>
            </div>
          ) : (
            <div className="table-wrapper">
              <table className="table">
                <thead>
                  <tr>
                    <th>ID</th>
                    <th>Título</th>
                    <th>Prioridad</th>
                    <th>Categoría</th>
                    <th>Estado</th>
                    <th>Asignado</th>
                    <th>Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  {cases.map((caso) => (
                    <tr key={caso.id_caso}>
                      <td style={{ fontWeight: 'bold' }}>{caso.id_caso}</td>
                      <td>
                        <div style={{ fontWeight: '500' }}>{caso.titulo_caso}</div>
                        <div style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
                          {caso.descripcion}
                        </div>
                      </td>
                      <td>
                        <span className={`badge badge-${caso.prioridad.toLowerCase()}`}>
                          {caso.prioridad}
                        </span>
                      </td>
                      <td>{getCategoryName(caso.id_categoria)}</td>
                      <td>
                        <span className={`status-dot status-${caso.id_estado}`}></span>
                        {getStateName(caso.id_estado)}
                      </td>
                      <td style={{ fontSize: '0.85rem' }}>
                        {caso.id_responsable_asignado ? `ID ${caso.id_responsable_asignado}` : 'Sin asignar'}
                      </td>
                      <td>
                        {deleteConfirmId === caso.id_caso ? (
                          <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                            <span style={{ fontSize: '0.75rem', color: '#fca5a5', fontWeight: 'bold' }}>¿Borrar?</span>
                            <button 
                              className="btn btn-danger btn-sm" 
                              style={{ padding: '0.2rem 0.5rem', fontSize: '0.8rem' }}
                              onClick={() => handleDeleteClick(caso.id_caso)}
                            >
                              Sí
                            </button>
                            <button 
                              className="btn btn-secondary btn-sm" 
                              style={{ padding: '0.2rem 0.5rem', fontSize: '0.8rem' }}
                              onClick={() => setDeleteConfirmId(null)}
                            >
                              No
                            </button>
                          </div>
                        ) : (
                          <div style={{ display: 'flex', gap: '0.5rem' }}>
                            <button 
                              className="btn btn-secondary btn-sm" 
                              onClick={() => handleEditClick(caso)}
                            >
                              ✏️ Editar
                            </button>
                            <button 
                              className="btn btn-danger btn-sm" 
                              onClick={() => setDeleteConfirmId(caso.id_caso)}
                            >
                              🗑️
                            </button>
                          </div>
                        )}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </section>

        {/* Right Side: Create/Update Form */}
        <section className="glass-panel" style={{ padding: '1.75rem' }}>
          <h2 className="section-title">
            {isEditing ? '✏️ Editar Caso' : '➕ Registrar Nuevo Caso'}
          </h2>

          <form onSubmit={handleCreateOrUpdateCase} style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            <div className="form-group">
              <label className="form-label">ID Caso (Numérico)</label>
              <input 
                type="number" 
                className="form-control" 
                value={caseId} 
                onChange={(e) => setCaseId(e.target.value)} 
                disabled={isEditing}
                placeholder="Ej: 1"
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Título del Caso</label>
              <input 
                type="text" 
                className="form-control" 
                value={caseTitle} 
                onChange={(e) => setCaseTitle(e.target.value)} 
                placeholder="Falla de conexión..."
                required
              />
            </div>

            <div className="form-group">
              <label className="form-label">Descripción Detallada</label>
              <textarea 
                className="form-control" 
                value={caseDesc} 
                onChange={(e) => setCaseDesc(e.target.value)} 
                rows="3"
                placeholder="Detalle técnico de la falla o solicitud..."
                required
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Prioridad</label>
                <select 
                  className="form-control" 
                  value={casePriority} 
                  onChange={(e) => setCasePriority(e.target.value)}
                >
                  <option value="Alta">Alta 🔴</option>
                  <option value="Media">Media 🟡</option>
                  <option value="Baja">Baja 🟢</option>
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">Categoría</label>
                <select 
                  className="form-control" 
                  value={caseCategory} 
                  onChange={(e) => setCaseCategory(e.target.value)}
                >
                  {categories.map((c) => (
                    <option key={c.id_categoria} value={c.id_categoria}>
                      {c.nombre_categoria}
                    </option>
                  ))}
                </select>
              </div>
            </div>

            <div className="form-row">
              <div className="form-group">
                <label className="form-label">Estado</label>
                <select 
                  className="form-control" 
                  value={caseState} 
                  onChange={(e) => setCaseState(e.target.value)}
                >
                  {states.map((s) => (
                    <option key={s.id_estado} value={s.id_estado}>
                      {s.nombre_estado}
                    </option>
                  ))}
                </select>
              </div>

              <div className="form-group">
                <label className="form-label">ID Responsable (Opcional)</label>
                <input 
                  type="number" 
                  className="form-control" 
                  value={caseResponsable} 
                  onChange={(e) => setCaseResponsable(e.target.value)} 
                  placeholder="Ej: 102"
                />
              </div>
            </div>

            <div style={{ display: 'flex', gap: '0.75rem', marginTop: '0.5rem' }}>
              <button type="submit" className="btn btn-primary" style={{ flex: 1 }}>
                {isEditing ? 'Guardar Cambios' : 'Crear Caso'}
              </button>
              {isEditing && (
                <button type="button" className="btn btn-secondary" onClick={clearCaseForm}>
                  Cancelar
                </button>
              )}
            </div>
          </form>
        </section>
      </div>

      {/* Full Width Bottom Panel: Audit Logs */}
      <section className="glass-panel" style={{ marginTop: '2.5rem', padding: '1.75rem' }}>
        <h2 className="section-title">
          <span>📜 Registro de Auditoría de MongoDB (Log de Cambios)</span>
          <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>
            Colección: <code style={{ color: 'var(--primary)' }}>historial_cambios_casos</code>
          </span>
        </h2>

        {auditLogs.length === 0 ? (
          <div className="empty-state" style={{ padding: '2rem' }}>
            <p>No hay eventos de auditoría registrados aún en MongoDB.</p>
            <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)' }}>
              Realiza una modificación en un caso (Update) o desactiva uno (Delete) para generar logs.
            </p>
          </div>
        ) : (
          <div className="audit-list">
            {auditLogs.map((log) => (
              <div className="audit-item" key={log.id_auditoria}>
                <div className="audit-meta">
                  <span>Auditoría ID: <strong>{log.id_auditoria}</strong> • Caso ID: <strong>{log.id_caso}</strong></span>
                  <span>{formatDate(log.fecha_cambio)}</span>
                </div>
                <div className="audit-change">
                  El usuario <span className="audit-user">{log.usuario_db}</span> modificó el campo{' '}
                  <span className="field-highlight">{log.campo_modificado}</span>:{' '}
                  <span className="value-old">
                    {log.valor_anterior === true ? 'Activo' : log.valor_anterior === false ? 'Inactivo' : String(log.valor_anterior)}
                  </span>{' '}
                  ➔{' '}
                  <span className="value-new">
                    {log.valor_nuevo === true ? 'Activo' : log.valor_nuevo === false ? 'Inactivo' : String(log.valor_nuevo)}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </section>
    </div>
  );
}

export default App;
