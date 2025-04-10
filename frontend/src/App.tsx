import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { Provider } from 'react-redux';
import { ThemeProvider, CssBaseline } from '@mui/material';
import { store } from './store';
import theme from './theme';

// Components
import Layout from './components/Layout';
import Login from './pages/Login';
import PatientList from './pages/PatientList';
import PatientDashboard from './pages/PatientDashboard';
import PrivateRoute from './components/PrivateRoute';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <Layout>
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route
                path="/patients"
                element={
                  <PrivateRoute>
                    <PatientList />
                  </PrivateRoute>
                }
              />
              <Route
                path="/patient/:id"
                element={
                  <PrivateRoute>
                    <PatientDashboard />
                  </PrivateRoute>
                }
              />
              <Route path="/" element={<Navigate to="/login" replace />} />
            </Routes>
          </Layout>
        </Router>
      </ThemeProvider>
    </Provider>
  );
};

export default App; 