import React, { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import {
  Box,
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemButton,
  CircularProgress,
  Alert,
} from '@mui/material';
import { RootState } from '../store';
import {
  fetchPatientsStart,
  fetchPatientsSuccess,
  fetchPatientsFailure,
  selectPatient,
} from '../store/slices/patientSlice';
import axios from 'axios';

const PatientList: React.FC = () => {
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { patients, loading, error } = useSelector((state: RootState) => state.patients);

  useEffect(() => {
    const fetchPatients = async () => {
      dispatch(fetchPatientsStart());
      try {
        const response = await axios.get('/api/patients');
        dispatch(fetchPatientsSuccess(response.data));
      } catch (err) {
        dispatch(fetchPatientsFailure('Failed to fetch patients'));
      }
    };

    fetchPatients();
  }, [dispatch]);

  const handlePatientClick = (patient: any) => {
    dispatch(selectPatient(patient));
    navigate(`/patient/${patient.id}`);
  };

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

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Patients
      </Typography>
      <Card>
        <CardContent>
          <List>
            {patients.map((patient) => (
              <ListItem key={patient.id} disablePadding>
                <ListItemButton onClick={() => handlePatientClick(patient)}>
                  <ListItemText
                    primary={patient.name}
                    secondary={`Aadhaar: ${patient.aadhaar}`}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>
    </Box>
  );
};

export default PatientList; 