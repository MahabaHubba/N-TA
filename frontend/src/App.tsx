import { useState, useEffect } from "react";
import { Login } from "./components/Auth/Login";
import { Register } from "./components/Auth/Register";
import { AuthContext } from "./context/AuthContext";
import { Me } from "./pages/Me";
import { useNotifications } from "./hooks/useNotifications";
import "bootstrap/dist/css/bootstrap.min.css";
import { Container, Row, Col, Card, Button } from "react-bootstrap";

function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem("token"));
  const [user, setUser] = useState<string | null>(localStorage.getItem("user"));
  const [showRegister, setShowRegister] = useState(true);
  const notifications = useNotifications(token);

  // Persist auth state in localStorage
  useEffect(() => {
    if (token) localStorage.setItem("token", token);
    else localStorage.removeItem("token");
  }, [token]);

  // Persist user state in localStorage
  useEffect(() => {
    if (user) localStorage.setItem("user", user);
    else localStorage.removeItem("user");
  }, [user]);

  return (
    <AuthContext.Provider value={{ token, setToken, user, setUser }}>
      {/* Notification section */}
      {notifications.length > 0 && (
        <div style={{ position: "fixed", top: "1rem", right: "1rem", zIndex: 9999, minWidth: "280px" }}>
          {notifications.map((note) => (
            <div key={note.id} className="alert alert-info py-2 px-3 mb-2 shadow-sm">
              🔔 {note.message}
            </div>
          ))}
        </div>
      )}

      {/* Full-height centering */}
      <div style={{ minHeight: "100vh", display: "flex", alignItems: "center", backgroundColor: "#f0f2f5" }}>
        <Container>
          <Row className="justify-content-center">
            <Col xs={12} sm={10} md={6} lg={5}>
              <Card className="p-4 shadow-sm">
                <h2 className="text-center mb-4">N-TA</h2>

                {!token ? (
                  <>
                    <h5 className="text-center text-muted mb-4">
                      {showRegister ? "Create an account" : "Welcome back"}
                    </h5>

                    {showRegister ? <Register /> : <Login />}

                    <div className="text-center mt-3">
                      {showRegister ? (
                        <small>
                          Already have an account?{" "}
                          <Button variant="link" className="p-0" onClick={() => setShowRegister(false)}>
                            Log in
                          </Button>
                        </small>
                      ) : (
                        <small>
                          Don't have an account?{" "}
                          <Button variant="link" className="p-0" onClick={() => setShowRegister(true)}>
                            Register
                          </Button>
                        </small>
                      )}
                    </div>
                  </>
                ) : (
                  <>
                    <h5 className="text-center mb-3">Welcome, {user}</h5>
                    <div className="d-grid mb-3">
                      <Button variant="outline-danger" onClick={() => { setToken(null); setUser(null); localStorage.clear(); }}>
                        Logout
                      </Button>
                    </div>
                    <Me />
                  </>
                )}
              </Card>
            </Col>
          </Row>
        </Container>
      </div>
    </AuthContext.Provider>
  );
}

export default App;