import React, { useEffect } from 'react';
import { useParams } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Card,
  CardContent,
  Typography,
  CircularProgress,
  Alert,
  Grid,
  Paper,
} from '@mui/material';
import { RootState } from '../store';
import axios from 'axios';

const PatientDashboard: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const dispatch = useDispatch();
  const { selectedPatient } = useSelector((state: RootState) => state.patients);
  const [loading, setLoading] = React.useState(false);
  const [error, setError] = React.useState<string | null>(null);

  useEffect(() => {
    const fetchPatientDetails = async () => {
      if (!selectedPatient) {
        setLoading(true);
        try {
          const response = await axios.get(`/api/patient/${id}`);
          // Update patient details in Redux store
          // dispatch(updatePatientDetails(response.data));
        } catch (err) {
          setError('Failed to fetch patient details');
        } finally {
          setLoading(false);
        }
      }
    };

    fetchPatientDetails();
  }, [id, selectedPatient, dispatch]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mt: 2 }}>
        {error}
      </Alert>
    );
  }

  if (!selectedPatient) {
    return (
      <Alert severity="warning" sx={{ mt: 2 }}>
        Patient not found
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Patient Dashboard
      </Typography>
      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Personal Information
              </Typography>
              <Typography variant="body1">
                <strong>Name:</strong> {selectedPatient.name}
              </Typography>
              <Typography variant="body1">
                <strong>Aadhaar:</strong> {selectedPatient.aadhaar}
              </Typography>
              <Typography variant="body1">
                <strong>Created At:</strong>{' '}
                {new Date(selectedPatient.created_at).toLocaleDateString()}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Medical History
              </Typography>
              <Paper
                variant="outlined"
                sx={{ p: 2, minHeight: 200, whiteSpace: 'pre-wrap' }}
              >
                {selectedPatient.history || 'No medical history available'}
              </Paper>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
};

export default PatientDashboard; 