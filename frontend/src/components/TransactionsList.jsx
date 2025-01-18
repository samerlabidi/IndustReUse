import React, { useState } from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  IconButton,
  Box,
  Tabs,
  Tab,
  CircularProgress,
  Alert,
  TextField,
  InputAdornment,
  Button,
  Menu,
  MenuItem,
  ListItemIcon,
  ListItemText,
} from '@mui/material';
import {
  Edit as EditIcon,
  Delete as DeleteIcon,
  Search as SearchIcon,
  FilterList as FilterIcon,
  LocalShipping as ShippingIcon,
  Store as PickupIcon,
  LocalShipping as DeliveryIcon,
  SortByAlpha as SortIcon,
  Event as DateIcon,
  Assignment as StatusIcon,
  Check as AcceptIcon,
  Close as RejectIcon,
  Cancel as CancelIcon,
} from '@mui/icons-material';
import { useAuth } from '../../hooks/useAuth';

const TransactionsList = ({ 
  transactions = [], 
  isLoading, 
  error,
  onAccept,
  onReject,
  onCancel
}) => {
  const [activeTab, setActiveTab] = useState(0);
  const { user } = useAuth();
  const [searchTerm, setSearchTerm] = useState('');
  const [filterAnchor, setFilterAnchor] = useState(null);
  const [filterType, setFilterType] = useState('none');

  const getDeliveryIcon = (method) => {
    switch (method.toLowerCase()) {
      case 'shipping':
        return <ShippingIcon color="primary" />;
      case 'pickup':
        return <PickupIcon color="primary" />;
      case 'delivery':
        return <DeliveryIcon color="primary" />;
      default:
        return <ShippingIcon color="primary" />;
    }
  };

  const handleFilterClick = (event) => {
    setFilterAnchor(event.currentTarget);
  };

  const handleFilterClose = () => {
    setFilterAnchor(null);
  };

  const handleFilterSelect = (type) => {
    setFilterType(type);
    handleFilterClose();
  };

  const filterTransactions = (transactions) => {
    let filtered = transactions;

    // Search filter
    if (searchTerm) {
      const searchLower = searchTerm.toLowerCase();
      filtered = filtered.filter(t => 
        t.material.name.toLowerCase().includes(searchLower) ||
        t.message?.toLowerCase().includes(searchLower) ||
        t.status.toLowerCase().includes(searchLower)
      );
    }

    // Sort filter
    switch (filterType) {
      case 'date':
        filtered.sort((a, b) => new Date(b.created_at) - new Date(a.created_at));
        break;
      case 'status':
        filtered.sort((a, b) => a.status.localeCompare(b.status));
        break;
      case 'material':
        filtered.sort((a, b) => a.material.name.localeCompare(b.material.name));
        break;
      default:
        break;
    }

    return filtered;
  };

  const myRequests = filterTransactions(transactions.filter(t => t.from_user.id === user?.id));
  const receivedRequests = filterTransactions(transactions.filter(t => t.to_user.id === user?.id));

  const currentTransactions = activeTab === 0 ? myRequests : receivedRequests;

  const renderActions = (transaction) => {
    console.log('Rendering actions for:', transaction);
    const status = transaction.status.toLowerCase();
    
    if (activeTab === 0) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1 }}>
          {status === 'pending' && (
            <IconButton 
              size="small" 
              color="error"
              onClick={() => onCancel(transaction.id)}
              title="Cancel Request"
            >
              <CancelIcon />
            </IconButton>
          )}
        </Box>
      );
    } else {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1 }}>
          {status === 'pending' && (
            <>
              <IconButton 
                size="small" 
                color="success"
                onClick={() => onAccept(transaction.id)}
                title="Accept Request"
              >
                <AcceptIcon />
              </IconButton>
              <IconButton 
                size="small" 
                color="error"
                onClick={() => onReject(transaction.id)}
                title="Reject Request"
              >
                <RejectIcon />
              </IconButton>
            </>
          )}
        </Box>
      );
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Tabs
        value={activeTab}
        onChange={(event, newValue) => setActiveTab(newValue)}
        sx={{ mb: 2 }}
      >
        <Tab label={`My Material Requests (${myRequests.length})`} />
        <Tab label={`Requests for My Materials (${receivedRequests.length})`} />
      </Tabs>

      <Box sx={{ mb: 3, display: 'flex', gap: 2 }}>
        <TextField
          size="small"
          placeholder="Search transactions..."
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
          sx={{ flexGrow: 1 }}
          InputProps={{
            startAdornment: (
              <InputAdornment position="start">
                <SearchIcon />
              </InputAdornment>
            ),
          }}
        />
        <Button
          variant="outlined"
          startIcon={<FilterIcon />}
          onClick={handleFilterClick}
        >
          {filterType === 'none' ? 'Filter' : `Sort by ${filterType}`}
        </Button>
        <Menu
          anchorEl={filterAnchor}
          open={Boolean(filterAnchor)}
          onClose={handleFilterClose}
        >
          <MenuItem onClick={() => handleFilterSelect('date')}>
            <ListItemIcon><DateIcon /></ListItemIcon>
            <ListItemText>Sort by Date</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => handleFilterSelect('status')}>
            <ListItemIcon><StatusIcon /></ListItemIcon>
            <ListItemText>Sort by Status</ListItemText>
          </MenuItem>
          <MenuItem onClick={() => handleFilterSelect('material')}>
            <ListItemIcon><SortIcon /></ListItemIcon>
            <ListItemText>Sort by Material</ListItemText>
          </MenuItem>
          {filterType !== 'none' && (
            <MenuItem onClick={() => handleFilterSelect('none')}>
              <ListItemText>Clear Sort</ListItemText>
            </MenuItem>
          )}
        </Menu>
      </Box>

      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow 
              sx={{ 
                backgroundColor: 'primary.main',
                '&:hover': {
                  backgroundColor: 'primary.main',
                },
                '& .MuiTableCell-head': {
                  color: '#FFFFFF !important',
                  fontWeight: 700,
                  fontSize: '0.95rem',
                  textAlign: 'center'
                }
              }}
            >
              <TableCell>Request ID</TableCell>
              <TableCell>Material Details</TableCell>
              <TableCell>Message</TableCell>
              <TableCell>Delivery Info</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {currentTransactions.map((transaction) => (
              <TableRow key={transaction.id}>
                <TableCell sx={{ textAlign: 'center' }}>
                  #{transaction.id}
                </TableCell>
                <TableCell sx={{ textAlign: 'center' }}>
                  <Box>
                    <strong>{transaction.material.name}</strong>
                    <br />
                    Quantity: {transaction.quantity}
                    <br />
                    {activeTab === 0 ? 
                      `To: ${transaction.to_user.username}` : 
                      `From: ${transaction.from_user.username}`}
                  </Box>
                </TableCell>
                <TableCell sx={{ textAlign: 'center' }}>
                  {transaction.message}
                </TableCell>
                <TableCell sx={{ textAlign: 'center' }}>
                  <Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1 }}>
                      {getDeliveryIcon(transaction.delivery_method)}
                      <strong>{transaction.delivery_method}</strong>
                    </Box>
                    {new Date(transaction.delivery_date).toLocaleDateString()}
                  </Box>
                </TableCell>
                <TableCell sx={{ textAlign: 'center' }}>
                  <Chip
                    label={transaction.status}
                    color={
                      transaction.status.toLowerCase() === 'accepted' ? 'success' :
                      transaction.status.toLowerCase() === 'pending' ? 'warning' :
                      transaction.status.toLowerCase() === 'rejected' ? 'error' :
                      transaction.status.toLowerCase() === 'completed' ? 'success' :
                      transaction.status.toLowerCase() === 'cancelled' ? 'error' : 'default'
                    }
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {renderActions(transaction)}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};

export default TransactionsList;