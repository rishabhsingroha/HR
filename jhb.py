import React, { useState, useEffect, useRef } from 'react';
import { X, Upload, Eye, EyeOff, FileText, Trash2, ChevronDown, MapPin, Search, Loader } from 'lucide-react';
import { RetailerManagmentService, DistributorServices, SubDistributorServices } from '../../services/apiService';

const AddDistributorModal = ({ onClose, onAdd, type = 'super_distributor', isEdit = false, userData = null }) => {
  const [activeTab, setActiveTab] = useState('basic');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [isLoadingAddress, setIsLoadingAddress] = useState(false);
  const [isLoadingSuperDistributors, setIsLoadingSuperDistributors] = useState(false);
  const [isLoadingDistributors, setIsLoadingDistributors] = useState(false);
  const [isLoadingSubDistributors, setIsLoadingSubDistributors] = useState(false);
  const [superDistributors, setSuperDistributors] = useState([]);
  const [distributors, setDistributors] = useState([]);
  const [subDistributors, setSubDistributors] = useState([]);
  const [allDistributors, setAllDistributors] = useState([]); // Store all distributors
  const [allSubDistributors, setAllSubDistributors] = useState([]); // Store all sub-distributors
  const [completedSections, setCompletedSections] = useState({
    basic: false,
    business: false,
    address: false,
    contact: false,
    documents: false,
    banking: false
  });

  // Google Maps refs
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markerRef = useRef(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);

  // Initialize services
  const retailerService = new RetailerManagmentService();
  const distributorService = new DistributorServices();
  const subDistributorService = new SubDistributorServices();

  // Fetch super distributors on component mount
  useEffect(() => {
    const fetchSuperDistributors = async () => {
      try {
        setIsLoadingSuperDistributors(true);
        const response = await retailerService.getSuperDistributors();
        if (response && response.data) {
          // Transform the data to match the expected format
          const formattedData = response.data.data.map(sd => ({
            id: sd._id || sd.id,
            name: sd.businessName || sd.name,
            code: sd.code || `SD-${sd._id}`
          }));
          setSuperDistributors(formattedData);
        }
      } catch (error) {
        console.error('Error fetching super distributors:', error);
      } finally {
        setIsLoadingSuperDistributors(false);
      }
    };

    if (type === 'distributor' || type === 'sub_distributor' || type === 'retailer') {
      fetchSuperDistributors();
    }
  }, [type]);

  // Fetch distributors on component mount
  useEffect(() => {
    const fetchDistributors = async () => {
      try {
        setIsLoadingDistributors(true);
        const response = await distributorService.getAll();
        if (response && response.data) {
          // Transform the data to match the expected format
          const formattedData = response.data.map(dist => ({
            id: dist._id || dist.id,
            name: dist.businessName || dist.name,
            code: dist.code || `D-${dist._id}`,
            superDistributor: dist.parentHierarchy?.superDistributorId || dist.superDistributorId
          }));
          setAllDistributors(formattedData);
        }
      } catch (error) {
        console.error('Error fetching distributors:', error);
      } finally {
        setIsLoadingDistributors(false);
      }
    };

    if (type === 'sub_distributor' || type === 'retailer') {
      fetchDistributors();
    }
  }, [type]);

  // Fetch sub-distributors on component mount
  useEffect(() => {
    const fetchSubDistributors = async () => {
      try {
        setIsLoadingSubDistributors(true);
        const response = await subDistributorService.getAll();
        if (response && response.data) {
          // Transform the data to match the expected format
          const formattedData = response.data.map(sub => ({
            id: sub._id || sub.id,
            name: sub.businessName || sub.name,
            code: sub.code || `SUB-${sub._id}`,
            distributorId: sub.parentHierarchy?.distributorId || sub.distributorId
          }));
          setAllSubDistributors(formattedData);
        }
      } catch (error) {
        console.error('Error fetching sub-distributors:', error);
      } finally {
        setIsLoadingSubDistributors(false);
      }
    };

    if (type === 'retailer') {
      fetchSubDistributors();
    }
  }, [type]);

  // Initialize form data based on edit mode
  const getInitialFormData = () => {
    if (isEdit && userData) {
      return {
        // Basic Information
        firstName: userData.ownerName?.split(' ')[0] || '',
        lastName: userData.ownerName?.split(' ')[1] || '',
        dateOfBirth: userData.dateOfBirth || '',
        anniversaryDate: userData.anniversaryDate || '',
        email: userData.email || '',
        password: '', // Never pre-fill password in edit mode
        confirmPassword: '',
        phoneNumber: userData.phone || '',
        alternatePhoneNumber: userData.alternatePhone || '',
        profileImage: userData.profileImage || null,
        username: userData.username || '',
        about: userData.about || '',
        joiningDate: userData.joiningDate || '',
        
        // Hierarchy fields
        selectedSuperDistributor: userData.parentHierarchy?.superDistributorId || '',
        selectedDistributor: userData.parentHierarchy?.distributorId || '',
        selectedSubDistributor: userData.parentHierarchy?.subDistributorsId || '',
        
        // Business Details
        businessName: userData.businessName || '',
        businessType: userData.businessType || '',
        gstNumber: userData.gstNumber || '',
        panNumber: userData.panNumber || '',
        businessRegistrationNumber: userData.businessRegistrationNumber || '',
        
        // Address Details
        businessAddress: userData.address?.street || '',
        businessCity: userData.address?.city || '',
        businessState: userData.address?.state || '',
        businessPincode: userData.address?.pincode || '',
        landmarks: userData.address?.landmarks || '',
        coordinates: userData.address?.coordinates ? {
          lat: userData.address.coordinates.coordinates[1],
          lng: userData.address.coordinates.coordinates[0]
        } : { lat: '', lng: '' },
        
        // Contact Details
        whatsappNumber: userData.whatsappNumber || '',
        businessPhoneNumber: userData.businessPhoneNumber || '',
        businessEmail: userData.businessEmail || '',
        contactPersonName: userData.contactPersonName || '',
        contactPersonDesignation: userData.contactPersonDesignation || '',
        emergencyContactName: userData.emergencyContactName || '',
        emergencyContactNumber: userData.emergencyContactNumber || '',
        emergencyContactRelation: userData.emergencyContactRelation || '',
        
        // Banking Details
        bankName: userData.bankDetails?.bankName || '',
        accountNumber: userData.bankDetails?.accountNumber || '',
        ifscCode: userData.bankDetails?.ifscCode || '',
        accountHolderName: userData.bankDetails?.accountHolderName || '',
        branchName: userData.bankDetails?.branchName || '',
        accountType: userData.accountType || '',
        
        // Documents
        documents: userData.documents?.map(doc => ({
          id: doc.id || Date.now() + Math.random(),
          name: doc.name || `${doc.type} Document`,
          type: doc.type || 'application/pdf',
          size: doc.size || 0,
          data: doc.url || doc.data,
          isExisting: true
        })) || []
      };
    }
    
    // Default empty form for add mode
    return {
      firstName: '',
      lastName: '',
      dateOfBirth: '',
      anniversaryDate: '',
      email: '',
      password: '',
      confirmPassword: '',
      phoneNumber: '',
      alternatePhoneNumber: '',
      profileImage: null,
      username: '',
      about: '',
      joiningDate: '',
      selectedSuperDistributor: '',
      selectedDistributor: '',
      selectedSubDistributor: '',
      businessName: '',
      businessType: '',
      gstNumber: '',
      panNumber: '',
      businessAddress: '',
      businessCity: '',
      businessState: '',
      businessPincode: '',
      landmarks: '',
      coordinates: { lat: '', lng: '' },
      businessRegistrationNumber: '',
      whatsappNumber: '',
      businessPhoneNumber: '',
      businessEmail: '',
      contactPersonName: '',
      contactPersonDesignation: '',
      emergencyContactName: '',
      emergencyContactNumber: '',
      emergencyContactRelation: '',
      bankName: '',
      accountNumber: '',
      ifscCode: '',
      accountHolderName: '',
      branchName: '',
      accountType: '',
      documents: []
    };
  };

  const [formData, setFormData] = useState(getInitialFormData);

  // Get modal configuration based on type and mode
  const getModalConfig = () => {
    const baseConfig = {
      super_distributor: { 
        title: isEdit ? 'Edit Super Distributor' : 'Add Super Distributor', 
        id: isEdit ? userData?.id || 'SD-EDIT' : 'SD-0024',
        buttonText: isEdit ? 'Update Super Distributor' : 'Save Super Distributor'
      },
      distributor: { 
        title: isEdit ? 'Edit Distributor' : 'Add Distributor', 
        id: isEdit ? userData?.id || 'D-EDIT' : 'D-0045',
        buttonText: isEdit ? 'Update Distributor' : 'Save Distributor'
      },
      sub_distributor: { 
        title: isEdit ? 'Edit Sub Distributor' : 'Add Sub Distributor', 
        id: isEdit ? userData?.id || 'SUB-EDIT' : 'SUB-0067',
        buttonText: isEdit ? 'Update Sub Distributor' : 'Save Sub Distributor'
      },
      retailer: { 
        title: isEdit ? 'Edit Retailer' : 'Add Retailer', 
        id: isEdit ? userData?.id || 'R-EDIT' : 'R-0156',
        buttonText: isEdit ? 'Update Retailer' : 'Save Retailer'
      }
    };
    
    return baseConfig[type] || baseConfig.super_distributor;
  };

  const modalConfig = getModalConfig();

  // Filter functions - now using API data
  const getFilteredDistributors = () => {
    if (!formData.selectedSuperDistributor) return [];
    return allDistributors.filter(dist => dist.superDistributor === formData.selectedSuperDistributor);
  };

  const getFilteredSubDistributors = () => {
    if (!formData.selectedDistributor) return [];
    return allSubDistributors.filter(sub => sub.distributorId === formData.selectedDistributor);
  };

  // Update filtered data when super distributor or distributor changes
  useEffect(() => {
    setDistributors(getFilteredDistributors());
  }, [formData.selectedSuperDistributor, allDistributors]);

  useEffect(() => {
    setSubDistributors(getFilteredSubDistributors());
  }, [formData.selectedDistributor, allSubDistributors]);

  // Load Google Maps Script
  const loadGoogleMapsScript = () => {
    return new Promise((resolve, reject) => {
      if (window.google && window.google.maps) {
        resolve();
        return;
      }

      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDMqcNgn374iQO-GJc9q6QFmqmOj1b4n9A&libraries=places,geometry`;
      script.async = true;
      script.defer = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Failed to load Google Maps'));
      document.head.appendChild(script);
    });
  };

  // Initialize Google Map
  const initializeMap = async () => {
    try {
      await loadGoogleMapsScript();
      
      if (!mapRef.current) return;

      const defaultCenter = { lat: 28.6139, lng: 77.2090 }; // Default to Delhi
      const center = (formData.coordinates.lat && formData.coordinates.lng) 
        ? { lat: parseFloat(formData.coordinates.lat), lng: parseFloat(formData.coordinates.lng) }
        : defaultCenter;

      const map = new window.google.maps.Map(mapRef.current, {
        zoom: 15,
        center: center,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
      });

      mapInstanceRef.current = map;

      // Add click listener to map
      map.addListener('click', (event) => {
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();
        
        updateMarkerPosition(lat, lng);
        reverseGeocode(lat, lng);
      });

      // Add marker if coordinates exist
      if (formData.coordinates.lat && formData.coordinates.lng) {
        addMarker(parseFloat(formData.coordinates.lat), parseFloat(formData.coordinates.lng));
      }

      setIsMapLoaded(true);
    } catch (error) {
      console.error('Error initializing map:', error);
      // Fallback: You can show an error message or use a different map service
    }
  };

  // Add or update marker on map
  const addMarker = (lat, lng) => {
    if (!mapInstanceRef.current) return;

    // Remove existing marker
    if (markerRef.current) {
      markerRef.current.setMap(null);
    }

    // Add new marker
    markerRef.current = new window.google.maps.Marker({
      position: { lat, lng },
      map: mapInstanceRef.current,
      draggable: true,
      title: 'Business Location'
    });

    // Add drag listener to marker
    markerRef.current.addListener('dragend', (event) => {
      const lat = event.latLng.lat();
      const lng = event.latLng.lng();
      updateMarkerPosition(lat, lng);
      reverseGeocode(lat, lng);
    });

    // Center map on marker
    mapInstanceRef.current.setCenter({ lat, lng });
  };

  // Update marker position and form data
  const updateMarkerPosition = (lat, lng) => {
    setFormData(prev => ({
      ...prev,
      coordinates: { lat: lat.toString(), lng: lng.toString() }
    }));
  };

  // Reverse geocode to get address from coordinates
  const reverseGeocode = async (lat, lng) => {
    if (!window.google) return;

    const geocoder = new window.google.maps.Geocoder();
    
    try {
      const response = await new Promise((resolve, reject) => {
        geocoder.geocode({ location: { lat, lng } }, (results, status) => {
          if (status === 'OK') {
            resolve(results);
          } else {
            reject(new Error('Geocoder failed: ' + status));
          }
        });
      });

      if (response && response[0]) {
        const result = response[0];
        const addressComponents = result.address_components;
        
        let city = '';
        let state = '';
        let pincode = '';
        let formattedAddress = result.formatted_address;

        // Extract address components
        addressComponents.forEach(component => {
          const types = component.types;
          if (types.includes('locality') || types.includes('administrative_area_level_2')) {
            city = component.long_name;
          }
          if (types.includes('administrative_area_level_1')) {
            state = component.long_name;
          }
          if (types.includes('postal_code')) {
            pincode = component.long_name;
          }
        });

        // Update form data
        setFormData(prev => ({
          ...prev,
          businessAddress: formattedAddress,
          businessCity: city,
          businessState: state,
          businessPincode: pincode
        }));
      }
    } catch (error) {
      console.error('Reverse geocoding failed:', error);
    }
  };

  // Fetch address data from pincode
  const handlePincodeChange = async (pincode) => {
    if (pincode.length === 6) {
      setIsLoadingAddress(true);
      
      try {
        // First try with Google Geocoding API
        if (window.google) {
          const geocoder = new window.google.maps.Geocoder();
          
          const response = await new Promise((resolve, reject) => {
            geocoder.geocode({ 
              address: `${pincode}, India`,
              componentRestrictions: { country: 'IN' }
            }, (results, status) => {
              if (status === 'OK') {
                resolve(results);
              } else {
                reject(new Error('Geocoding failed: ' + status));
              }
            });
          });

          if (response && response[0]) {
            const result = response[0];
            const location = result.geometry.location;
            const addressComponents = result.address_components;
            
            let city = '';
            let state = '';

            addressComponents.forEach(component => {
              const types = component.types;
              if (types.includes('locality') || types.includes('administrative_area_level_2')) {
                city = component.long_name;
              }
              if (types.includes('administrative_area_level_1')) {
                state = component.long_name;
              }
            });

            const lat = location.lat();
            const lng = location.lng();

            setFormData(prev => ({
              ...prev,
              businessCity: city,
              businessState: state,
              coordinates: { lat: lat.toString(), lng: lng.toString() }
            }));

            // Update map and marker
            if (mapInstanceRef.current) {
              addMarker(lat, lng);
            }
          }
        } else {
          // Fallback to mock data if Google Maps is not loaded
          const mockAddressData = {
            '110001': { city: 'New Delhi', state: 'Delhi', lat: 28.6139, lng: 77.2090 },
            '400001': { city: 'Mumbai', state: 'Maharashtra', lat: 19.0760, lng: 72.8777 },
            '560001': { city: 'Bangalore', state: 'Karnataka', lat: 12.9716, lng: 77.5946 },
            '122001': { city: 'Gurgaon', state: 'Haryana', lat: 28.4595, lng: 77.0266 }
          };
          
          const addressData = mockAddressData[pincode];
          if (addressData) {
            setFormData(prev => ({
              ...prev,
              businessCity: addressData.city,
              businessState: addressData.state,
              coordinates: { lat: addressData.lat.toString(), lng: addressData.lng.toString() }
            }));
          }
        }
      } catch (error) {
        console.error('Error fetching address data:', error);
        
        // Fallback to mock data
        const mockAddressData = {
          '110001': { city: 'New Delhi', state: 'Delhi', lat: 28.6139, lng: 77.2090 },
          '400001': { city: 'Mumbai', state: 'Maharashtra', lat: 19.0760, lng: 72.8777 },
          '560001': { city: 'Bangalore', state: 'Karnataka', lat: 12.9716, lng: 77.5946 },
          '122001': { city: 'Gurgaon', state: 'Haryana', lat: 28.4595, lng: 77.0266 }
        };
        
        const addressData = mockAddressData[pincode];
        if (addressData) {
          setFormData(prev => ({
            ...prev,
            businessCity: addressData.city,
            businessState: addressData.state,
            coordinates: { lat: addressData.lat.toString(), lng: addressData.lng.toString() }
          }));
        }
      } finally {
        setIsLoadingAddress(false);
      }
    }
  };

  // Input validation and formatting
  const handleNumberInput = (field, value) => {
    let processedValue = value;
    
    // Phone number fields - only digits, max 10
    if (field.includes('phoneNumber') || field.includes('PhoneNumber') || 
        field.includes('whatsappNumber') || field.includes('emergencyContactNumber')) {
      processedValue = value.replace(/[^0-9]/g, '').slice(0, 10);
    }
    
    // Pincode - only digits, max 6
    if (field === 'businessPincode') {
      processedValue = value.replace(/[^0-9]/g, '').slice(0, 6);
      // Auto-fill address on pincode change
      if (processedValue.length === 6) {
        handlePincodeChange(processedValue);
      }
    }

    // Account number - alphanumeric only
    if (field === 'accountNumber') {
      processedValue = value.replace(/[^a-zA-Z0-9]/g, '');
    }

    // GST number - alphanumeric uppercase, max 15
    if (field === 'gstNumber') {
      processedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 15);
    }

    // PAN number - alphanumeric uppercase, max 10
    if (field === 'panNumber') {
      processedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 10);
    }

    // IFSC code - alphanumeric uppercase, max 11
    if (field === 'ifscCode') {
      processedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 11);
    }

    return processedValue;
  };

  const handleInputChange = (field, value) => {
    const processedValue = handleNumberInput(field, value);
    
    setFormData(prev => {
      const newData = { ...prev, [field]: processedValue };
      
      // Reset distributor selection when super distributor changes
      if (field === 'selectedSuperDistributor') {
        newData.selectedDistributor = '';
        newData.selectedSubDistributor = '';
      }
      
      // Reset sub-distributor selection when distributor changes
      if (field === 'selectedDistributor') {
        newData.selectedSubDistributor = '';
      }
      
      return newData;
    });

    // Clear any existing errors for this field
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // Validation functions
  const validateBasicSection = () => {
    const baseFields = formData.firstName && 
                      formData.email && 
                      formData.phoneNumber && 
                      formData.phoneNumber.length === 10;

    // Password validation only for add mode
    const passwordValid = isEdit || (formData.password && 
                                    formData.confirmPassword && 
                                    formData.password === formData.confirmPassword);

    // Additional hierarchy validation
    if (type === 'retailer') {
      return baseFields && passwordValid && formData.selectedSuperDistributor && 
             formData.selectedDistributor && formData.selectedSubDistributor;
    }
    
    if (type === 'sub_distributor') {
      return baseFields && passwordValid && formData.selectedSuperDistributor && formData.selectedDistributor;
    }
    
    if (type === 'distributor') {
      return baseFields && passwordValid && formData.selectedSuperDistributor;
    }
    
    return baseFields && passwordValid;
  };

  const validateBusinessSection = () => {
    return formData.businessName && 
           formData.businessType
  };

  const validateAddressSection = () => {
    return formData.businessAddress &&
           formData.businessCity &&
           formData.businessState &&
           formData.landmarks &&
           formData.businessPincode &&
           formData.businessPincode.length === 6 &&
           formData.coordinates.lat &&
           formData.coordinates.lng;
  };

  const validateContactSection = () => {
    return formData.emergencyContactName && 
           formData.emergencyContactNumber && 
           formData.emergencyContactRelation &&
           formData.emergencyContactNumber.length === 10;
  };

  const validateDocumentsSection = () => {
    return formData.documents.length > 0;
  };

  const validateBankingSection = () => {
    return formData.bankName && 
           formData.accountNumber && 
           formData.ifscCode && 
           formData.accountHolderName &&
           formData.ifscCode.length === 11;
  };

  // Check section completion
  const checkSectionCompletion = (section) => {
    let isComplete = false;
    
    switch (section) {
      case 'basic':
        isComplete = validateBasicSection();
        break;
      case 'business':
        isComplete = validateBusinessSection();
        break;
      case 'address':
        isComplete = validateAddressSection();
        break;
      case 'contact':
        isComplete = validateContactSection();
        break;
      case 'documents':
        isComplete = validateDocumentsSection();
        break;
      case 'banking':
        isComplete = validateBankingSection();
        break;
      default:
        isComplete = false;
    }

    setCompletedSections(prev => ({
      ...prev,
      [section]: isComplete
    }));

    return isComplete;
  };

  // Check if section can be accessed
  const canAccessSection = (targetSection) => {
    const tabs = ['basic', 'business', 'address', 'contact', 'documents', 'banking'];
    const targetIndex = tabs.indexOf(targetSection);
    const currentIndex = tabs.indexOf(activeTab);
    
    // Allow access to current and previous sections
    if (targetIndex <= currentIndex) return true;
    
    // Check if all previous sections are completed
    for (let i = 0; i < targetIndex; i++) {
      if (!completedSections[tabs[i]]) {
        return false;
      }
    }
    return true;
  };

  // Enhanced Map Component
  const MapView = () => {
    return (
      <div className="space-y-4">
        {!isMapLoaded && (
          <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
            <div className="text-center">
              <Loader className="h-8 w-8 text-gray-400 mx-auto mb-2 animate-spin" />
              <p className="text-gray-500">Loading Google Maps...</p>
            </div>
          </div>
        )}
        
        <div 
          ref={mapRef} 
          className={`w-full h-64 rounded-lg border ${!isMapLoaded ? 'hidden' : 'block'}`}
          style={{ minHeight: '256px' }}
        />
        
        {isMapLoaded && (
          <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
            <p className="font-medium text-blue-800 mb-1">How to use the map:</p>
            <ul className="text-blue-700 space-y-1">
              <li>• Click anywhere on the map to set the business location</li>
              <li>• Drag the marker to adjust the exact position</li>
              <li>• Address details will be automatically filled</li>
            </ul>
          </div>
        )}

        {formData.coordinates.lat && formData.coordinates.lng && (
          <div className="bg-green-50 p-3 rounded-lg border border-green-200">
            <p className="text-sm text-green-800">
              <MapPin className="inline w-4 h-4 mr-1" />
              Selected Location: {formData.coordinates.lat}, {formData.coordinates.lng}
            </p>
            {formData.businessCity && formData.businessState && (
              <p className="text-sm text-green-700 mt-1">
                📍 {formData.businessCity}, {formData.businessState}
              </p>
            )}
          </div>
        )}
      </div>
    );
  };

  // Define renderSuperDistributorDropdown function before the return statement
  const renderSuperDistributorDropdown = () => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Select Super Distributor <span className="text-red-500">*</span>
      </label>
      <div className="relative">
        <select
          value={formData.selectedSuperDistributor}
          onChange={(e) => handleInputChange('selectedSuperDistributor', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none pr-8"
          required
          disabled={isLoadingSuperDistributors}
        >
          <option value="">Choose Super Distributor</option>
          {superDistributors.map((sd) => (
            <option key={sd.id} value={sd.id}>
              {sd.code} - {sd.name}
            </option>
          ))}
        </select>
              { isLoadingSuperDistributors ? (
          <Loader className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 animate-spin" size={16} />
        ) : (
          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={16} />
        )}
      </div>
      {isLoadingSuperDistributors && (
        <p className="text-xs text-gray-500 mt-1">Loading super distributors...</p>
        )}
    </div>
  );

  // Form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate all sections before submission
    const allSectionsValid = validateBasicSection() && 
                            validateBusinessSection() && 
                            validateAddressSection() &&
                            validateContactSection() && 
                            validateDocumentsSection() && 
                            validateBankingSection();
    
    if (!allSectionsValid) {
      alert('Please complete all required fields in all sections.');
      return;
    }

    // Prepare submission data in the required format
    const submissionData = {
      ...(isEdit && { id: userData?.id }),
      userType: type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
      businessName: formData.businessName,
      ownerName: `${formData.firstName} ${formData.lastName}`.trim(),
      email: formData.email,
      phone: formData.phoneNumber,
      alternatePhone: formData.alternatePhoneNumber,
      ...(type === "Retailer"
        ? { retailerConfig: {} }
        : { distributorConfig: {} }),
      address: {
        street: formData.businessAddress,
        city: formData.businessCity,
        state: formData.businessState,
        pincode: formData.businessPincode,
        country: "India",
        landmarks: formData.landmarks,
        coordinates: {
          type: "Point",
          coordinates: [parseFloat(formData.coordinates.lng), parseFloat(formData.coordinates.lat)]
        }
      },
      parentHierarchy: {
        ...(formData.selectedSuperDistributor && { superDistributorId: formData.selectedSuperDistributor }),
        ...(formData.selectedDistributor && { distributorId: formData.selectedDistributor }),
        ...(formData.selectedSubDistributor && { subDistributorsId: formData.selectedSubDistributor })
      },
      businessType: formData.businessType,
      panNumber: formData.panNumber,
      gstNumber: formData.gstNumber,
      dateOfBirth: formData.dateOfBirth,
      anniversaryDate: formData.anniversaryDate,
      bankDetails: {
        accountNumber: formData.accountNumber,
        ifscCode: formData.ifscCode,
        bankName: formData.bankName,
        branchName: formData.branchName,
        accountHolderName: formData.accountHolderName
      },
      documents: formData.documents.map(doc => ({
        type: doc.name.includes('GST') ? 'GST' : 
              doc.name.includes('PAN') ? 'PAN' : 'OTHER',
        url: doc.data,
        name: doc.name,
        isVerified: false
      })),
      tags: ["premium", "north-zone"],
      notes: `${isEdit ? 'Updated' : 'Created'} ${type} profile`,
      ...(isEdit ? { updatedAt: new Date().toISOString() } : { createdAt: new Date().toISOString() })
    };
    
    onAdd(submissionData);
    onClose();
  };

  // File handling
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 4 * 1024 * 1024) {
        alert('Image size should be less than 4MB');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setFormData(prev => ({
          ...prev,
          profileImage: e.target.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDocumentUpload = (e) => {
    const files = Array.from(e.target.files);
    
    files.forEach(file => {
      if (file.size <= 4 * 1024 * 1024) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const newDocument = {
            id: Date.now() + Math.random(),
            name: file.name,
            type: file.type,
            size: file.size,
            data: e.target.result,
            isExisting: false
          };
          
          setFormData(prev => ({
            ...prev,
            documents: [...prev.documents, newDocument]
          }));
        };
        reader.readAsDataURL(file);
      } else {
        alert(`File ${file.name} is too large. Please upload files under 4MB.`);
      }
    });
  };

  const removeDocument = (docId) => {
    setFormData(prev => ({
      ...prev,
      documents: prev.documents.filter(doc => doc.id !== docId)
    }));
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Navigation
  const goToNextTab = () => {
    const tabs = ['basic', 'business', 'address', 'contact', 'documents', 'banking'];
    const currentIndex = tabs.indexOf(activeTab);
    if (currentIndex < tabs.length - 1) {
      setActiveTab(tabs[currentIndex + 1]);
    }
  };

  const goToPreviousTab = () => {
    const tabs = ['basic', 'business', 'address', 'contact', 'documents', 'banking'];
    const currentIndex = tabs.indexOf(activeTab);
    if (currentIndex > 0) {
      setActiveTab(tabs[currentIndex - 1]);
    }
  };

  // Effect to check section completion when form data changes
  useEffect(() => {
    checkSectionCompletion(activeTab);
  }, [formData, activeTab]);

  // Initialize map when address tab is opened
  useEffect(() => {
    if (activeTab === 'address' && !isMapLoaded) {
      initializeMap();
    }
  }, [activeTab]);

  // Update map when coordinates change
  useEffect(() => {
    if (isMapLoaded && formData.coordinates.lat && formData.coordinates.lng) {
      const lat = parseFloat(formData.coordinates.lat);
      const lng = parseFloat(formData.coordinates.lng);
      if (!isNaN(lat) && !isNaN(lng)) {
        addMarker(lat, lng);
      }
    }
  }, [formData.coordinates, isMapLoaded]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-5xl max-h-[95vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">{modalConfig.title}</h2>
            <p className="text-sm text-gray-500">
              {type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} ID: {modalConfig.id}
            </p>
            {isEdit && (
              <span className="inline-block mt-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                Edit Mode
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-100"
          >
            <X size={20} />
          </button>
        </div>

        {/* Tabs Navigation */}
        <div className="border-b border-gray-200">
          <div className="flex overflow-x-auto">
            {['basic', 'business', 'address', 'contact', 'documents', 'banking'].map((tab) => (
              <button
                key={tab}
                onClick={() => canAccessSection(tab) && setActiveTab(tab)}
                disabled={!canAccessSection(tab)}
                className={`px-6 py-3 text-sm font-medium whitespace-nowrap relative transition-colors ${
                  activeTab === tab
                    ? 'text-orange-600 border-b-2 border-orange-600 bg-orange-50'
                    : canAccessSection(tab)
                    ? 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                    : 'text-gray-300 cursor-not-allowed'
                }`}
              >
                {tab === 'basic' ? 'Basic Information' :
                 tab === 'business' ? 'Business Details' :
                 tab === 'address' ? 'Address Details' :
                 tab === 'contact' ? 'Contact Details' :
                 tab === 'documents' ? 'Documents' : 'Banking Details'}
                
                {completedSections[tab] && (
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full"></span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Form Content */}
        <div className="p-6 max-h-[65vh] overflow-y-auto">
          {/* Basic Information Tab */}
          {activeTab === 'basic' && (
            <div className="space-y-6">
              {/* Profile Image Upload */}
              <div className="flex items-center space-x-4">
                <div className="w-20 h-20 bg-gray-100 rounded-lg flex items-center justify-center overflow-hidden">
                  {formData.profileImage ? (
                    <img src={formData.profileImage} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                      <div className="w-8 h-8 bg-orange-500 rounded-full"></div>
                    </div>
                  )}
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Upload Profile Image</h3>
                  <p className="text-xs text-gray-500 mb-2">Image should be below 4 MB</p>
                  <div className="flex space-x-2">
                    <label className="bg-orange-500 text-white px-3 py-1 rounded text-sm cursor-pointer hover:bg-orange-600 transition-colors">
                      Upload
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                      />
                    </label>
                    <button
                      type="button"
                      className="border border-gray-300 px-3 py-1 rounded text-sm hover:bg-gray-50 transition-colors"
                      onClick={() => setFormData(prev => ({ ...prev, profileImage: null }))}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>

              {/* Hierarchy Selection */}
              {(type === 'retailer' || type === 'distributor' || type === 'sub_distributor') && (
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h3 className="text-sm font-medium text-blue-800 mb-3">
                    Hierarchy Selection
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Super Distributor Selection */}
                    {renderSuperDistributorDropdown()}

                    {/* Distributor Selection - For Sub Distributor and Retailer */}
                    {(type === 'sub_distributor' || type === 'retailer') && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Select Distributor <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <select
                            value={formData.selectedDistributor}
                            onChange={(e) => handleInputChange('selectedDistributor', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none pr-8"
                            disabled={!formData.selectedSuperDistributor}
                            required
                          >
                            <option value="">Choose Distributor</option>
                            {getFilteredDistributors().map((dist) => (
                              <option key={dist.id} value={dist.id}>
                                {dist.code} - {dist.name}
                              </option>
                            ))}
                          </select>
                          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={16} />
                        </div>
                        {!formData.selectedSuperDistributor && (
                          <p className="text-xs text-gray-500 mt-1">Please select a Super Distributor first</p>
                        )}
                      </div>
                    )}

                    {/* Sub Distributor Selection - Only for Retailer */}
                    {type === 'retailer' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Select Sub Distributor <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <select
                            value={formData.selectedSubDistributor}
                            onChange={(e) => handleInputChange('selectedSubDistributor', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none pr-8"
                            disabled={!formData.selectedDistributor}
                            required
                          >
                            <option value="">Choose Sub Distributor</option>
                            {getFilteredSubDistributors().map((sub) => (
                              <option key={sub.id} value={sub.id}>
                                {sub.code} - {sub.name}
                              </option>
                            ))}
                          </select>
                          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={16} />
                        </div>
                        {!formData.selectedDistributor && (
                          <p className="text-xs text-gray-500 mt-1">Please select a Distributor first</p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Personal Information Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    First Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) => handleInputChange('firstName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter first name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Last Name
                  </label>
                  <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) => handleInputChange('lastName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter last name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter email address"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    value={formData.phoneNumber}
                    onChange={(e) => handleInputChange('phoneNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter 10-digit phone number"
                    required
                  />
                  {formData.phoneNumber && formData.phoneNumber.length > 0 && formData.phoneNumber.length !== 10 && (
                    <p className="text-xs text-red-500 mt-1">Phone number must be exactly 10 digits</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date of Birth
                  </label>
                  <input
                    type="date"
                    value={formData.dateOfBirth}
                    onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Anniversary Date
                  </label>
                  <input
                    type="date"
                    value={formData.anniversaryDate}
                    onChange={(e) => handleInputChange('anniversaryDate', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>

                {/* Password fields - only show in add mode */}
                {!isEdit && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Password <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type={showPassword ? "text" : "password"}
                          value={formData.password}
                          onChange={(e) => handleInputChange('password', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent pr-10"
                          placeholder="Enter password"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Confirm Password <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type={showConfirmPassword ? "text" : "password"}
                          value={formData.confirmPassword}
                          onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent pr-10"
                          placeholder="Confirm password"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                      {formData.password && formData.confirmPassword && formData.password !== formData.confirmPassword && (
                        <p className="text-xs text-red-500 mt-1">Passwords do not match</p>
                      )}
                    </div>
                  </>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  About
                </label>
                <textarea
                  value={formData.about}
                  onChange={(e) => handleInputChange('about', e.target.value)}
                  rows="4"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="Tell us about yourself..."
                />
              </div>
            </div>
          )}

          {/* Business Details Tab */}
          {activeTab === 'business' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.businessName}
                    onChange={(e) => handleInputChange('businessName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter business name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Type <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={formData.businessType}
                    onChange={(e) => handleInputChange('businessType', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select Business Type</option>
                    <option value="Sole Proprietorship">Sole Proprietorship</option>
                    <option value="Partnership">Partnership</option>
                    <option value="Private Limited">Private Limited</option>
                    <option value="LLP">Limited Liability Partnership</option>
                    <option value="Public Limited">Public Limited</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    GST Number
                  </label>
                  <input
                    type="text"
                    value={formData.gstNumber}
                    onChange={(e) => handleInputChange('gstNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="27AAPFU0939F1ZV"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    PAN Number
                  </label>
                  <input
                    type="text"
                    value={formData.panNumber}
                    onChange={(e) => handleInputChange('panNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="AAPFU0939F"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Registration Number
                  </label>
                  <input
                    type="text"
                    value={formData.businessRegistrationNumber}
                    onChange={(e) => handleInputChange('businessRegistrationNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter registration number"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Address Details Tab */}
          {activeTab === 'address' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Address Form */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Business Address <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={formData.businessAddress}
                      onChange={(e) => handleInputChange('businessAddress', e.target.value)}
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                      placeholder="Enter complete business address"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Pincode <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type="text"
                          value={formData.businessPincode}
                          onChange={(e) => handleInputChange('businessPincode', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent pr-10"
                          placeholder="Enter 6-digit pincode"
                          required
                        />
                        {isLoadingAddress && (
                          <Loader className="absolute right-3 top-1/2 transform -translate-y-1/2 text-orange-500 animate-spin" size={16} />
                        )}
                      </div>
                      {formData.businessPincode && formData.businessPincode.length > 0 && formData.businessPincode.length !== 6 && (
                        <p className="text-xs text-red-500 mt-1">Pincode must be exactly 6 digits</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        City <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        value={formData.businessCity}
                        onChange={(e) => handleInputChange('businessCity', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                        placeholder="Auto-filled from pincode"
                        required
                        readOnly
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      State <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.businessState}
                      onChange={(e) => handleInputChange('businessState', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                      placeholder="Auto-filled from pincode"
                      required
                      readOnly
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Landmarks <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.landmarks}
                      onChange={(e) => handleInputChange('landmarks', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                      placeholder="e.g., Near City Mall, Opposite Bank"
                      required
                    />
                  </div>
                </div>

                {/* Map View */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Location on Map <span className="text-red-500">*</span>
                  </label>
                  <MapView />
                </div>
              </div>
            </div>
          )}

          {/* Contact Details Tab */}
          {activeTab === 'contact' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Alternate Phone Number
                  </label>
                  <input
                    type="tel"
                    value={formData.alternatePhoneNumber}
                    onChange={(e) => handleInputChange('alternatePhoneNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter alternate phone number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    WhatsApp Number
                  </label>
                  <input
                    type="tel"
                    value={formData.whatsappNumber}
                    onChange={(e) => handleInputChange('whatsappNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter WhatsApp number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Phone Number
                  </label>
                  <input
                    type="tel"
                    value={formData.businessPhoneNumber}
                    onChange={(e) => handleInputChange('businessPhoneNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter business phone number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Email
                  </label>
                  <input
                    type="email"
                    value={formData.businessEmail}
                    onChange={(e) => handleInputChange('businessEmail', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter business email"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Contact Person Name
                  </label>
                  <input
                    type="text"
                    value={formData.contactPersonName}
                    onChange={(e) => handleInputChange('contactPersonName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter contact person name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Contact Person Designation
                  </label>
                  <input
                    type="text"
                    value={formData.contactPersonDesignation}
                    onChange={(e) => handleInputChange('contactPersonDesignation', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter designation"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Emergency Contact Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.emergencyContactName}
                    onChange={(e) => handleInputChange('emergencyContactName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter emergency contact name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Emergency Contact Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    value={formData.emergencyContactNumber}
                    onChange={(e) => handleInputChange('emergencyContactNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter emergency contact number"
                    required
                  />
                  {formData.emergencyContactNumber && formData.emergencyContactNumber.length > 0 && formData.emergencyContactNumber.length !== 10 && (
                    <p className="text-xs text-red-500 mt-1">Phone number must be exactly 10 digits</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Emergency Contact Relation <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={formData.emergencyContactRelation}
                    onChange={(e) => handleInputChange('emergencyContactRelation', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select Relation</option>
                    <option value="Father">Father</option>
                    <option value="Mother">Mother</option>
                    <option value="Spouse">Spouse</option>
                    <option value="Brother">Brother</option>
                    <option value="Sister">Sister</option>
                    <option value="Friend">Friend</option>
                    <option value="Business Partner">Business Partner</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Documents Tab */}
          {activeTab === 'documents' && (
            <div className="space-y-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-orange-400 transition-colors">
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Upload Documents</h3>
                <p className="text-sm text-gray-500 mb-4">
                  Upload GST certificate, PAN card, business registration, bank statements, and other relevant documents
                </p>
                <p className="text-xs text-gray-400 mb-4">
                  Supported formats: PDF, DOC, DOCX, JPG, PNG (Max size: 4MB each)
                </p>
                <label className="bg-orange-500 text-white px-6 py-2 rounded-lg cursor-pointer hover:bg-orange-600 inline-flex items-center gap-2 transition-colors">
                  <Upload size={16} />
                  Choose Files
                  <input
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                    onChange={handleDocumentUpload}
                    className="hidden"
                  />
                </label>
              </div>

              {/* Uploaded Documents List */}
              {formData.documents.length > 0 && (
                <div className="space-y-3">
                  <h4 className="font-medium text-gray-900">
                    {isEdit ? 'Documents' : 'Uploaded Documents'} ({formData.documents.length})
                  </h4>
                  {formData.documents.map((doc) => (
                    <div key={doc.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-8 w-8 text-orange-500" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                          <div className="flex items-center space-x-2">
                            <p className="text-xs text-gray-500">{formatFileSize(doc.size)}</p>
                            {doc.isExisting && (
                              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                                Existing
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={() => removeDocument(doc.id)}
                        className="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-50 transition-colors"
                        title="Remove document"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Banking Details Tab */}
          {activeTab === 'banking' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Bank Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.bankName}
                    onChange={(e) => handleInputChange('bankName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter bank name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Account Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.accountNumber}
                    onChange={(e) => handleInputChange('accountNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter account number"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    IFSC Code <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.ifscCode}
                    onChange={(e) => handleInputChange('ifscCode', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="SBIN0001234"
                    required
                  />
                  {formData.ifscCode && formData.ifscCode.length > 0 && formData.ifscCode.length !== 11 && (
                    <p className="text-xs text-red-500 mt-1">IFSC code must be exactly 11 characters</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Account Holder Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.accountHolderName}
                    onChange={(e) => handleInputChange('accountHolderName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter account holder name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Branch Name
                  </label>
                  <input
                    type="text"
                    value={formData.branchName}
                    onChange={(e) => handleInputChange('branchName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter branch name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Account Type
                  </label>
                  <select
                    value={formData.accountType}
                    onChange={(e) => handleInputChange('accountType', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  >
                    <option value="">Select Account Type</option>
                    <option value="Savings">Savings Account</option>
                    <option value="Current">Current Account</option>
                    <option value="Business">Business Account</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 px-6 py-4 bg-gray-50">
          <div className="flex justify-between items-center">
            <div>
              {activeTab !== 'basic' && (
                <button
                  type="button"
                  onClick={goToPreviousTab}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Previous
                </button>
              )}
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              
              {activeTab !== 'banking' ? (
                <button
                  type="button"
                  disabled={!completedSections[activeTab]}
                  onClick={goToNextTab}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    completedSections[activeTab]
                      ? 'bg-orange-500 text-white hover:bg-orange-600' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Next
                </button>
              ) : (
                <button
                  type="submit"
                  onClick={handleSubmit}
                  disabled={!completedSections.banking}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    completedSections.banking
                      ? 'bg-green-500 text-white hover:bg-green-600'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  {modalConfig.buttonText}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddDistributorModal;
                           




















































import React, { useState, useEffect, useRef } from 'react';
import { X, Upload, Eye, EyeOff, FileText, Trash2, ChevronDown, MapPin, Search, Loader } from 'lucide-react';
import { RetailerManagmentService, DistributorServices, SubDistributorServices } from '../../services/apiService';

const AddDistributorModal = ({ onClose, onAdd, type = 'super_distributor', isEdit = false, userData = null }) => {
  const [activeTab, setActiveTab] = useState('basic');
  const [showPassword, setShowPassword] = useState(false);
  const [showConfirmPassword, setShowConfirmPassword] = useState(false);
  const [errors, setErrors] = useState({});
  const [isLoadingAddress, setIsLoadingAddress] = useState(false);
  const [isLoadingSuperDistributors, setIsLoadingSuperDistributors] = useState(false);
  const [isLoadingDistributors, setIsLoadingDistributors] = useState(false);
  const [isLoadingSubDistributors, setIsLoadingSubDistributors] = useState(false);
  const [superDistributors, setSuperDistributors] = useState([]);
  const [distributors, setDistributors] = useState([]);
  const [subDistributors, setSubDistributors] = useState([]);
  const [allDistributors, setAllDistributors] = useState([]); // Store all distributors
  const [allSubDistributors, setAllSubDistributors] = useState([]); // Store all sub-distributors
  const [completedSections, setCompletedSections] = useState({
    basic: false,
    business: false,
    address: false,
    contact: false,
    documents: false,
    banking: false
  });

  // Google Maps refs
  const mapRef = useRef(null);
  const mapInstanceRef = useRef(null);
  const markerRef = useRef(null);
  const [isMapLoaded, setIsMapLoaded] = useState(false);

  // Initialize services
  const retailerService = new RetailerManagmentService();
  const distributorService = new DistributorServices();
  const subDistributorService = new SubDistributorServices();

  // Fetch super distributors on component mount
  useEffect(() => {
    const fetchSuperDistributors = async () => {
      try {
        setIsLoadingSuperDistributors(true);
        const response = await retailerService.getSuperDistributors();
        if (response && response.data) {
          // Transform the data to match the expected format
          const formattedData = response.data.data.map(sd => ({
            id: sd._id || sd.id,
            name: sd.businessName || sd.name,
            code: sd.code || `SD-${sd._id}`
          }));
          setSuperDistributors(formattedData);
        }
      } catch (error) {
        console.error('Error fetching super distributors:', error);
      } finally {
        setIsLoadingSuperDistributors(false);
      }
    };

    if (type === 'distributor' || type === 'sub_distributor' || type === 'retailer') {
      fetchSuperDistributors();
    }
  }, [type]);

  // Fetch distributors on component mount
  useEffect(() => {
    const fetchDistributors = async () => {
      try {
        setIsLoadingDistributors(true);
        const response = await distributorService.getAll();
        if (response && response.data) {
          // Transform the data to match the expected format
          const formattedData = response.data.map(dist => ({
            id: dist._id || dist.id,
            name: dist.businessName || dist.name,
            code: dist.code || `D-${dist._id}`,
            superDistributor: dist.parentHierarchy?.superDistributorId || dist.superDistributorId
          }));
          setAllDistributors(formattedData);
        }
      } catch (error) {
        console.error('Error fetching distributors:', error);
      } finally {
        setIsLoadingDistributors(false);
      }
    };

    if (type === 'sub_distributor' || type === 'retailer') {
      fetchDistributors();
    }
  }, [type]);

  // Fetch sub-distributors on component mount
  useEffect(() => {
    const fetchSubDistributors = async () => {
      try {
        setIsLoadingSubDistributors(true);
        const response = await subDistributorService.getAll();
        if (response && response.data) {
          // Transform the data to match the expected format
          const formattedData = response.data.map(sub => ({
            id: sub._id || sub.id,
            name: sub.businessName || sub.name,
            code: sub.code || `SUB-${sub._id}`,
            distributorId: sub.parentHierarchy?.distributorId || sub.distributorId
          }));
          setAllSubDistributors(formattedData);
        }
      } catch (error) {
        console.error('Error fetching sub-distributors:', error);
      } finally {
        setIsLoadingSubDistributors(false);
      }
    };

    if (type === 'retailer') {
      fetchSubDistributors();
    }
  }, [type]);
  // Sample data for dropdowns
  const [distributors] = useState([
    { id: 'D001', name: 'City Distribution Center', code: 'D-001', superDistributor: 'SD001' },
    { id: 'D002', name: 'Regional Supply Chain', code: 'D-002', superDistributor: 'SD001' },
    { id: 'D003', name: 'Local Trading Post', code: 'D-003', superDistributor: 'SD002' },
    { id: 'D004', name: 'Urban Distribution Hub', code: 'D-004', superDistributor: 'SD002' },
    { id: 'D005', name: 'Premium Distributors', code: 'D-005', superDistributor: 'SD003' },
    { id: 'D006', name: 'Fast Track Distribution', code: 'D-006', superDistributor: 'SD004' }
  ]);

  const [subDistributors] = useState([
    { id: 'SUB001', name: 'Sub Dist A', code: 'SUB-001', distributorId: 'D001' },
    { id: 'SUB002', name: 'Sub Dist B', code: 'SUB-002', distributorId: 'D001' },
    { id: 'SUB003', name: 'Sub Dist C', code: 'SUB-003', distributorId: 'D002' }
  ]);

  // Initialize form data based on edit mode
  const getInitialFormData = () => {
    if (isEdit && userData) {
      return {
        // Basic Information
        firstName: userData.ownerName?.split(' ')[0] || '',
        lastName: userData.ownerName?.split(' ')[1] || '',
        dateOfBirth: userData.dateOfBirth || '',
        anniversaryDate: userData.anniversaryDate || '',
        email: userData.email || '',
        password: '', // Never pre-fill password in edit mode
        confirmPassword: '',
        phoneNumber: userData.phone || '',
        alternatePhoneNumber: userData.alternatePhone || '',
        profileImage: userData.profileImage || null,
        username: userData.username || '',
        about: userData.about || '',
        joiningDate: userData.joiningDate || '',
        
        // Hierarchy fields
        selectedSuperDistributor: userData.parentHierarchy?.superDistributorId || '',
        selectedDistributor: userData.parentHierarchy?.distributorId || '',
        selectedSubDistributor: userData.parentHierarchy?.subDistributorsId || '',
        
        // Business Details
        businessName: userData.businessName || '',
        businessType: userData.businessType || '',
        gstNumber: userData.gstNumber || '',
        panNumber: userData.panNumber || '',
        businessRegistrationNumber: userData.businessRegistrationNumber || '',
        
        // Address Details
        businessAddress: userData.address?.street || '',
        businessCity: userData.address?.city || '',
        businessState: userData.address?.state || '',
        businessPincode: userData.address?.pincode || '',
        landmarks: userData.address?.landmarks || '',
        coordinates: userData.address?.coordinates ? {
          lat: userData.address.coordinates.coordinates[1],
          lng: userData.address.coordinates.coordinates[0]
        } : { lat: '', lng: '' },
        
        // Contact Details
        whatsappNumber: userData.whatsappNumber || '',
        businessPhoneNumber: userData.businessPhoneNumber || '',
        businessEmail: userData.businessEmail || '',
        contactPersonName: userData.contactPersonName || '',
        contactPersonDesignation: userData.contactPersonDesignation || '',
        emergencyContactName: userData.emergencyContactName || '',
        emergencyContactNumber: userData.emergencyContactNumber || '',
        emergencyContactRelation: userData.emergencyContactRelation || '',
        
        // Banking Details
        bankName: userData.bankDetails?.bankName || '',
        accountNumber: userData.bankDetails?.accountNumber || '',
        ifscCode: userData.bankDetails?.ifscCode || '',
        accountHolderName: userData.bankDetails?.accountHolderName || '',
        branchName: userData.bankDetails?.branchName || '',
        accountType: userData.accountType || '',
        
        // Documents
        documents: userData.documents?.map(doc => ({
          id: doc.id || Date.now() + Math.random(),
          name: doc.name || `${doc.type} Document`,
          type: doc.type || 'application/pdf',
          size: doc.size || 0,
          data: doc.url || doc.data,
          isExisting: true
        })) || []
      };
    }
    
    // Default empty form for add mode
    return {
      firstName: '',
      lastName: '',
      dateOfBirth: '',
      anniversaryDate: '',
      email: '',
      password: '',
      confirmPassword: '',
      phoneNumber: '',
      alternatePhoneNumber: '',
      profileImage: null,
      username: '',
      about: '',
      joiningDate: '',
      selectedSuperDistributor: '',
      selectedDistributor: '',
      selectedSubDistributor: '',
      businessName: '',
      businessType: '',
      gstNumber: '',
      panNumber: '',
      businessAddress: '',
      businessCity: '',
      businessState: '',
      businessPincode: '',
      landmarks: '',
      coordinates: { lat: '', lng: '' },
      businessRegistrationNumber: '',
      whatsappNumber: '',
      businessPhoneNumber: '',
      businessEmail: '',
      contactPersonName: '',
      contactPersonDesignation: '',
      emergencyContactName: '',
      emergencyContactNumber: '',
      emergencyContactRelation: '',
      bankName: '',
      accountNumber: '',
      ifscCode: '',
      accountHolderName: '',
      branchName: '',
      accountType: '',
      documents: []
    };
  };

  const [formData, setFormData] = useState(getInitialFormData);

  // Get modal configuration based on type and mode
  const getModalConfig = () => {
    const baseConfig = {
      super_distributor: { 
        title: isEdit ? 'Edit Super Distributor' : 'Add Super Distributor', 
        id: isEdit ? userData?.id || 'SD-EDIT' : 'SD-0024',
        buttonText: isEdit ? 'Update Super Distributor' : 'Save Super Distributor'
      },
      distributor: { 
        title: isEdit ? 'Edit Distributor' : 'Add Distributor', 
        id: isEdit ? userData?.id || 'D-EDIT' : 'D-0045',
        buttonText: isEdit ? 'Update Distributor' : 'Save Distributor'
      },
      sub_distributor: { 
        title: isEdit ? 'Edit Sub Distributor' : 'Add Sub Distributor', 
        id: isEdit ? userData?.id || 'SUB-EDIT' : 'SUB-0067',
        buttonText: isEdit ? 'Update Sub Distributor' : 'Save Sub Distributor'
      },
      retailer: { 
        title: isEdit ? 'Edit Retailer' : 'Add Retailer', 
        id: isEdit ? userData?.id || 'R-EDIT' : 'R-0156',
        buttonText: isEdit ? 'Update Retailer' : 'Save Retailer'
      }
    };
    
    return baseConfig[type] || baseConfig.super_distributor;
  };

  const modalConfig = getModalConfig();

  // Filter functions
  const getFilteredDistributors = () => {
    if (!formData.selectedSuperDistributor) return [];
    return distributors.filter(dist => dist.superDistributor === formData.selectedSuperDistributor);
  };

  const getFilteredSubDistributors = () => {
    if (!formData.selectedDistributor) return [];
    return subDistributors.filter(sub => sub.distributorId === formData.selectedDistributor);
  };

  // Load Google Maps Script
  const loadGoogleMapsScript = () => {
    return new Promise((resolve, reject) => {
      if (window.google && window.google.maps) {
        resolve();
        return;
      }

      const script = document.createElement('script');
      script.src = `https://maps.googleapis.com/maps/api/js?key=AIzaSyDMqcNgn374iQO-GJc9q6QFmqmOj1b4n9A&libraries=places,geometry`;
      script.async = true;
      script.defer = true;
      script.onload = () => resolve();
      script.onerror = () => reject(new Error('Failed to load Google Maps'));
      document.head.appendChild(script);
    });
  };

  // Initialize Google Map
  const initializeMap = async () => {
    try {
      await loadGoogleMapsScript();
      
      if (!mapRef.current) return;

      const defaultCenter = { lat: 28.6139, lng: 77.2090 }; // Default to Delhi
      const center = (formData.coordinates.lat && formData.coordinates.lng) 
        ? { lat: parseFloat(formData.coordinates.lat), lng: parseFloat(formData.coordinates.lng) }
        : defaultCenter;

      const map = new window.google.maps.Map(mapRef.current, {
        zoom: 15,
        center: center,
        mapTypeControl: true,
        streetViewControl: true,
        fullscreenControl: true,
      });

      mapInstanceRef.current = map;

      // Add click listener to map
      map.addListener('click', (event) => {
        const lat = event.latLng.lat();
        const lng = event.latLng.lng();
        
        updateMarkerPosition(lat, lng);
        reverseGeocode(lat, lng);
      });

      // Add marker if coordinates exist
      if (formData.coordinates.lat && formData.coordinates.lng) {
        addMarker(parseFloat(formData.coordinates.lat), parseFloat(formData.coordinates.lng));
      }

      setIsMapLoaded(true);
    } catch (error) {
      console.error('Error initializing map:', error);
      // Fallback: You can show an error message or use a different map service
    }
  };

  // Add or update marker on map
  const addMarker = (lat, lng) => {
    if (!mapInstanceRef.current) return;

    // Remove existing marker
    if (markerRef.current) {
      markerRef.current.setMap(null);
    }

    // Add new marker
    markerRef.current = new window.google.maps.Marker({
      position: { lat, lng },
      map: mapInstanceRef.current,
      draggable: true,
      title: 'Business Location'
    });

    // Add drag listener to marker
    markerRef.current.addListener('dragend', (event) => {
      const lat = event.latLng.lat();
      const lng = event.latLng.lng();
      updateMarkerPosition(lat, lng);
      reverseGeocode(lat, lng);
    });

    // Center map on marker
    mapInstanceRef.current.setCenter({ lat, lng });
  };

  // Update marker position and form data
  const updateMarkerPosition = (lat, lng) => {
    setFormData(prev => ({
      ...prev,
      coordinates: { lat: lat.toString(), lng: lng.toString() }
    }));
  };

  // Reverse geocode to get address from coordinates
  const reverseGeocode = async (lat, lng) => {
    if (!window.google) return;

    const geocoder = new window.google.maps.Geocoder();
    
    try {
      const response = await new Promise((resolve, reject) => {
        geocoder.geocode({ location: { lat, lng } }, (results, status) => {
          if (status === 'OK') {
            resolve(results);
          } else {
            reject(new Error('Geocoder failed: ' + status));
          }
        });
      });

      if (response && response[0]) {
        const result = response[0];
        const addressComponents = result.address_components;
        
        let city = '';
        let state = '';
        let pincode = '';
        let formattedAddress = result.formatted_address;

        // Extract address components
        addressComponents.forEach(component => {
          const types = component.types;
          if (types.includes('locality') || types.includes('administrative_area_level_2')) {
            city = component.long_name;
          }
          if (types.includes('administrative_area_level_1')) {
            state = component.long_name;
          }
          if (types.includes('postal_code')) {
            pincode = component.long_name;
          }
        });

        // Update form data
        setFormData(prev => ({
          ...prev,
          businessAddress: formattedAddress,
          businessCity: city,
          businessState: state,
          businessPincode: pincode
        }));
      }
    } catch (error) {
      console.error('Reverse geocoding failed:', error);
    }
  };

  // Fetch address data from pincode
  const handlePincodeChange = async (pincode) => {
    if (pincode.length === 6) {
      setIsLoadingAddress(true);
      
      try {
        // First try with Google Geocoding API
        if (window.google) {
          const geocoder = new window.google.maps.Geocoder();
          
          const response = await new Promise((resolve, reject) => {
            geocoder.geocode({ 
              address: `${pincode}, India`,
              componentRestrictions: { country: 'IN' }
            }, (results, status) => {
              if (status === 'OK') {
                resolve(results);
              } else {
                reject(new Error('Geocoding failed: ' + status));
              }
            });
          });

          if (response && response[0]) {
            const result = response[0];
            const location = result.geometry.location;
            const addressComponents = result.address_components;
            
            let city = '';
            let state = '';

            addressComponents.forEach(component => {
              const types = component.types;
              if (types.includes('locality') || types.includes('administrative_area_level_2')) {
                city = component.long_name;
              }
              if (types.includes('administrative_area_level_1')) {
                state = component.long_name;
              }
            });

            const lat = location.lat();
            const lng = location.lng();

            setFormData(prev => ({
              ...prev,
              businessCity: city,
              businessState: state,
              coordinates: { lat: lat.toString(), lng: lng.toString() }
            }));

            // Update map and marker
            if (mapInstanceRef.current) {
              addMarker(lat, lng);
            }
          }
        } else {
          // Fallback to mock data if Google Maps is not loaded
          const mockAddressData = {
            '110001': { city: 'New Delhi', state: 'Delhi', lat: 28.6139, lng: 77.2090 },
            '400001': { city: 'Mumbai', state: 'Maharashtra', lat: 19.0760, lng: 72.8777 },
            '560001': { city: 'Bangalore', state: 'Karnataka', lat: 12.9716, lng: 77.5946 },
            '122001': { city: 'Gurgaon', state: 'Haryana', lat: 28.4595, lng: 77.0266 }
          };
          
          const addressData = mockAddressData[pincode];
          if (addressData) {
            setFormData(prev => ({
              ...prev,
              businessCity: addressData.city,
              businessState: addressData.state,
              coordinates: { lat: addressData.lat.toString(), lng: addressData.lng.toString() }
            }));
          }
        }
      } catch (error) {
        console.error('Error fetching address data:', error);
        
        // Fallback to mock data
        const mockAddressData = {
          '110001': { city: 'New Delhi', state: 'Delhi', lat: 28.6139, lng: 77.2090 },
          '400001': { city: 'Mumbai', state: 'Maharashtra', lat: 19.0760, lng: 72.8777 },
          '560001': { city: 'Bangalore', state: 'Karnataka', lat: 12.9716, lng: 77.5946 },
          '122001': { city: 'Gurgaon', state: 'Haryana', lat: 28.4595, lng: 77.0266 }
        };
        
        const addressData = mockAddressData[pincode];
        if (addressData) {
          setFormData(prev => ({
            ...prev,
            businessCity: addressData.city,
            businessState: addressData.state,
            coordinates: { lat: addressData.lat.toString(), lng: addressData.lng.toString() }
          }));
        }
      } finally {
        setIsLoadingAddress(false);
      }
    }
  };

  // Input validation and formatting
  const handleNumberInput = (field, value) => {
    let processedValue = value;
    
    // Phone number fields - only digits, max 10
    if (field.includes('phoneNumber') || field.includes('PhoneNumber') || 
        field.includes('whatsappNumber') || field.includes('emergencyContactNumber')) {
      processedValue = value.replace(/[^0-9]/g, '').slice(0, 10);
    }
    
    // Pincode - only digits, max 6
    if (field === 'businessPincode') {
      processedValue = value.replace(/[^0-9]/g, '').slice(0, 6);
      // Auto-fill address on pincode change
      if (processedValue.length === 6) {
        handlePincodeChange(processedValue);
      }
    }

    // Account number - alphanumeric only
    if (field === 'accountNumber') {
      processedValue = value.replace(/[^a-zA-Z0-9]/g, '');
    }

    // GST number - alphanumeric uppercase, max 15
    if (field === 'gstNumber') {
      processedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 15);
    }

    // PAN number - alphanumeric uppercase, max 10
    if (field === 'panNumber') {
      processedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 10);
    }

    // IFSC code - alphanumeric uppercase, max 11
    if (field === 'ifscCode') {
      processedValue = value.toUpperCase().replace(/[^A-Z0-9]/g, '').slice(0, 11);
    }

    return processedValue;
  };

  const handleInputChange = (field, value) => {
    const processedValue = handleNumberInput(field, value);
    
    setFormData(prev => {
      const newData = { ...prev, [field]: processedValue };
      
      // Reset distributor selection when super distributor changes
      if (field === 'selectedSuperDistributor') {
        newData.selectedDistributor = '';
        newData.selectedSubDistributor = '';
      }
      
      // Reset sub-distributor selection when distributor changes
      if (field === 'selectedDistributor') {
        newData.selectedSubDistributor = '';
      }
      
      return newData;
    });

    // Clear any existing errors for this field
    if (errors[field]) {
      setErrors(prev => ({ ...prev, [field]: '' }));
    }
  };

  // Validation functions
  const validateBasicSection = () => {
    const baseFields = formData.firstName && 
                      formData.email && 
                      formData.phoneNumber && 
                      formData.phoneNumber.length === 10;

    // Password validation only for add mode
    const passwordValid = isEdit || (formData.password && 
                                    formData.confirmPassword && 
                                    formData.password === formData.confirmPassword);

    // Additional hierarchy validation
    if (type === 'retailer') {
      return baseFields && passwordValid && formData.selectedSuperDistributor && 
             formData.selectedDistributor && formData.selectedSubDistributor;
    }
    
    if (type === 'sub_distributor') {
      return baseFields && passwordValid && formData.selectedSuperDistributor && formData.selectedDistributor;
    }
    
    if (type === 'distributor') {
      return baseFields && passwordValid && formData.selectedSuperDistributor;
    }
    
    return baseFields && passwordValid;
  };

  const validateBusinessSection = () => {
    return formData.businessName && 
           formData.businessType
  };

  const validateAddressSection = () => {
    return formData.businessAddress &&
           formData.businessCity &&
           formData.businessState &&
           formData.landmarks &&
           formData.businessPincode &&
           formData.businessPincode.length === 6 &&
           formData.coordinates.lat &&
           formData.coordinates.lng;
  };

  const validateContactSection = () => {
    return formData.emergencyContactName && 
           formData.emergencyContactNumber && 
           formData.emergencyContactRelation &&
           formData.emergencyContactNumber.length === 10;
  };

  const validateDocumentsSection = () => {
    return formData.documents.length > 0;
  };

  const validateBankingSection = () => {
    return formData.bankName && 
           formData.accountNumber && 
           formData.ifscCode && 
           formData.accountHolderName &&
           formData.ifscCode.length === 11;
  };

  // Check section completion
  const checkSectionCompletion = (section) => {
    let isComplete = false;
    
    switch (section) {
      case 'basic':
        isComplete = validateBasicSection();
        break;
      case 'business':
        isComplete = validateBusinessSection();
        break;
      case 'address':
        isComplete = validateAddressSection();
        break;
      case 'contact':
        isComplete = validateContactSection();
        break;
      case 'documents':
        isComplete = validateDocumentsSection();
        break;
      case 'banking':
        isComplete = validateBankingSection();
        break;
      default:
        isComplete = false;
    }

    setCompletedSections(prev => ({
      ...prev,
      [section]: isComplete
    }));

    return isComplete;
  };

  // Check if section can be accessed
  const canAccessSection = (targetSection) => {
    const tabs = ['basic', 'business', 'address', 'contact', 'documents', 'banking'];
    const targetIndex = tabs.indexOf(targetSection);
    const currentIndex = tabs.indexOf(activeTab);
    
    // Allow access to current and previous sections
    if (targetIndex <= currentIndex) return true;
    
    // Check if all previous sections are completed
    for (let i = 0; i < targetIndex; i++) {
      if (!completedSections[tabs[i]]) {
        return false;
      }
    }
    return true;
  };

  // Enhanced Map Component
  const MapView = () => {
    return (
      <div className="space-y-4">
        {!isMapLoaded && (
          <div className="w-full h-64 bg-gray-100 rounded-lg flex items-center justify-center border-2 border-dashed border-gray-300">
            <div className="text-center">
              <Loader className="h-8 w-8 text-gray-400 mx-auto mb-2 animate-spin" />
              <p className="text-gray-500">Loading Google Maps...</p>
            </div>
          </div>
        )}
        
        <div 
          ref={mapRef} 
          className={`w-full h-64 rounded-lg border ${!isMapLoaded ? 'hidden' : 'block'}`}
          style={{ minHeight: '256px' }}
        />
        
        {isMapLoaded && (
          <div className="text-sm text-gray-600 bg-blue-50 p-3 rounded-lg">
            <p className="font-medium text-blue-800 mb-1">How to use the map:</p>
            <ul className="text-blue-700 space-y-1">
              <li>• Click anywhere on the map to set the business location</li>
              <li>• Drag the marker to adjust the exact position</li>
              <li>• Address details will be automatically filled</li>
            </ul>
          </div>
        )}

        {formData.coordinates.lat && formData.coordinates.lng && (
          <div className="bg-green-50 p-3 rounded-lg border border-green-200">
            <p className="text-sm text-green-800">
              <MapPin className="inline w-4 h-4 mr-1" />
              Selected Location: {formData.coordinates.lat}, {formData.coordinates.lng}
            </p>
            {formData.businessCity && formData.businessState && (
              <p className="text-sm text-green-700 mt-1">
                📍 {formData.businessCity}, {formData.businessState}
              </p>
            )}
          </div>
        )}
      </div>
    );
  };

  // Define renderSuperDistributorDropdown function before the return statement
  const renderSuperDistributorDropdown = () => (
    <div>
      <label className="block text-sm font-medium text-gray-700 mb-1">
        Select Super Distributor <span className="text-red-500">*</span>
      </label>
      <div className="relative">
        <select
          value={formData.selectedSuperDistributor}
          onChange={(e) => handleInputChange('selectedSuperDistributor', e.target.value)}
          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none pr-8"
          required
          disabled={isLoadingSuperDistributors}
        >
          <option value="">Choose Super Distributor</option>
          {superDistributors.map((sd) => (
            <option key={sd.id} value={sd.id}>
              {sd.code} - {sd.name}
            </option>
          ))}
        </select>
        {isLoadingSuperDistributors ? (
          <Loader className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 animate-spin" size={16} />
        ) : (
          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={16} />
        )}
      </div>
      {isLoadingSuperDistributors && (
        <p className="text-xs text-gray-500 mt-1">Loading super distributors...</p>
      )}
    </div>
  );

  // Form submission
  const handleSubmit = (e) => {
    e.preventDefault();
    
    // Validate all sections before submission
    const allSectionsValid = validateBasicSection() && 
                            validateBusinessSection() && 
                            validateAddressSection() &&
                            validateContactSection() && 
                            validateDocumentsSection() && 
                            validateBankingSection();
    
    if (!allSectionsValid) {
      alert('Please complete all required fields in all sections.');
      return;
    }

    // Prepare submission data in the required format
    const submissionData = {
      ...(isEdit && { id: userData?.id }),
      userType: type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' '),
      businessName: formData.businessName,
      ownerName: `${formData.firstName} ${formData.lastName}`.trim(),
      email: formData.email,
      phone: formData.phoneNumber,
      alternatePhone: formData.alternatePhoneNumber,
      ...(type === "Retailer"
        ? { retailerConfig: {} }
        : { distributorConfig: {} }),
      address: {
        street: formData.businessAddress,
        city: formData.businessCity,
        state: formData.businessState,
        pincode: formData.businessPincode,
        country: "India",
        landmarks: formData.landmarks,
        coordinates: {
          type: "Point",
          coordinates: [parseFloat(formData.coordinates.lng), parseFloat(formData.coordinates.lat)]
        }
      },
      parentHierarchy: {
        ...(formData.selectedSuperDistributor && { superDistributorId: formData.selectedSuperDistributor }),
        ...(formData.selectedDistributor && { distributorId: formData.selectedDistributor }),
        ...(formData.selectedSubDistributor && { subDistributorsId: formData.selectedSubDistributor })
      },
      businessType: formData.businessType,
      panNumber: formData.panNumber,
      gstNumber: formData.gstNumber,
      dateOfBirth: formData.dateOfBirth,
      anniversaryDate: formData.anniversaryDate,
      bankDetails: {
        accountNumber: formData.accountNumber,
        ifscCode: formData.ifscCode,
        bankName: formData.bankName,
        branchName: formData.branchName,
        accountHolderName: formData.accountHolderName
      },
      documents: formData.documents.map(doc => ({
        type: doc.name.includes('GST') ? 'GST' : 
              doc.name.includes('PAN') ? 'PAN' : 'OTHER',
        url: doc.data,
        name: doc.name,
        isVerified: false
      })),
      tags: ["premium", "north-zone"],
      notes: `${isEdit ? 'Updated' : 'Created'} ${type} profile`,
      ...(isEdit ? { updatedAt: new Date().toISOString() } : { createdAt: new Date().toISOString() })
    };
    
    onAdd(submissionData);
    onClose();
  };

  // File handling
  const handleImageUpload = (e) => {
    const file = e.target.files[0];
    if (file) {
      if (file.size > 4 * 1024 * 1024) {
        alert('Image size should be less than 4MB');
        return;
      }
      
      const reader = new FileReader();
      reader.onload = (e) => {
        setFormData(prev => ({
          ...prev,
          profileImage: e.target.result
        }));
      };
      reader.readAsDataURL(file);
    }
  };

  const handleDocumentUpload = (e) => {
    const files = Array.from(e.target.files);
    
    files.forEach(file => {
      if (file.size <= 4 * 1024 * 1024) {
        const reader = new FileReader();
        reader.onload = (e) => {
          const newDocument = {
            id: Date.now() + Math.random(),
            name: file.name,
            type: file.type,
            size: file.size,
            data: e.target.result,
            isExisting: false
          };
          
          setFormData(prev => ({
            ...prev,
            documents: [...prev.documents, newDocument]
          }));
        };
        reader.readAsDataURL(file);
      } else {
        alert(`File ${file.name} is too large. Please upload files under 4MB.`);
      }
    });
  };

  const removeDocument = (docId) => {
    setFormData(prev => ({
      ...prev,
      documents: prev.documents.filter(doc => doc.id !== docId)
    }));
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
  };

  // Navigation
  const goToNextTab = () => {
    const tabs = ['basic', 'business', 'address', 'contact', 'documents', 'banking'];
    const currentIndex = tabs.indexOf(activeTab);
    if (currentIndex < tabs.length - 1) {
      setActiveTab(tabs[currentIndex + 1]);
    }
  };

  const goToPreviousTab = () => {
    const tabs = ['basic', 'business', 'address', 'contact', 'documents', 'banking'];
    const currentIndex = tabs.indexOf(activeTab);
    if (currentIndex > 0) {
      setActiveTab(tabs[currentIndex - 1]);
    }
  };

  // Effect to check section completion when form data changes
  useEffect(() => {
    checkSectionCompletion(activeTab);
  }, [formData, activeTab]);

  // Initialize map when address tab is opened
  useEffect(() => {
    if (activeTab === 'address' && !isMapLoaded) {
      initializeMap();
    }
  }, [activeTab]);

  // Update map when coordinates change
  useEffect(() => {
    if (isMapLoaded && formData.coordinates.lat && formData.coordinates.lng) {
      const lat = parseFloat(formData.coordinates.lat);
      const lng = parseFloat(formData.coordinates.lng);
      if (!isNaN(lat) && !isNaN(lng)) {
        addMarker(lat, lng);
      }
    }
  }, [formData.coordinates, isMapLoaded]);

  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50 p-4">
      <div className="bg-white rounded-lg w-full max-w-5xl max-h-[95vh] overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between p-6 border-b border-gray-200">
          <div>
            <h2 className="text-xl font-semibold text-gray-800">{modalConfig.title}</h2>
            <p className="text-sm text-gray-500">
              {type.split('_').map(word => word.charAt(0).toUpperCase() + word.slice(1)).join(' ')} ID: {modalConfig.id}
            </p>
            {isEdit && (
              <span className="inline-block mt-1 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded-full">
                Edit Mode
              </span>
            )}
          </div>
          <button
            onClick={onClose}
            className="text-gray-400 hover:text-gray-600 p-1 rounded-full hover:bg-gray-100"
          >
            <X size={20} />
          </button>
        </div>

        {/* Tabs Navigation */}
        <div className="border-b border-gray-200">
          <div className="flex overflow-x-auto">
            {['basic', 'business', 'address', 'contact', 'documents', 'banking'].map((tab) => (
              <button
                key={tab}
                onClick={() => canAccessSection(tab) && setActiveTab(tab)}
                disabled={!canAccessSection(tab)}
                className={`px-6 py-3 text-sm font-medium whitespace-nowrap relative transition-colors ${
                  activeTab === tab
                    ? 'text-orange-600 border-b-2 border-orange-600 bg-orange-50'
                    : canAccessSection(tab)
                    ? 'text-gray-500 hover:text-gray-700 hover:bg-gray-50'
                    : 'text-gray-300 cursor-not-allowed'
                }`}
              >
                {tab === 'basic' ? 'Basic Information' :
                 tab === 'business' ? 'Business Details' :
                 tab === 'address' ? 'Address Details' :
                 tab === 'contact' ? 'Contact Details' :
                 tab === 'documents' ? 'Documents' : 'Banking Details'}
                
                {completedSections[tab] && (
                  <span className="absolute -top-1 -right-1 w-3 h-3 bg-green-500 rounded-full"></span>
                )}
              </button>
            ))}
          </div>
        </div>

        {/* Form Content */}
        <div className="p-6 max-h-[65vh] overflow-y-auto">
          {/* Basic Information Tab */}
          {activeTab === 'basic' && (
            <div className="space-y-6">
              {/* Profile Image Upload */}
              <div className="flex items-center space-x-4">
                <div className="w-20 h-20 bg-gray-100 rounded-lg flex items-center justify-center overflow-hidden">
                  {formData.profileImage ? (
                    <img src={formData.profileImage} alt="Profile" className="w-full h-full object-cover" />
                  ) : (
                    <div className="w-12 h-12 bg-orange-100 rounded-lg flex items-center justify-center">
                      <div className="w-8 h-8 bg-orange-500 rounded-full"></div>
                    </div>
                  )}
                </div>
                <div>
                  <h3 className="text-sm font-medium text-gray-700">Upload Profile Image</h3>
                  <p className="text-xs text-gray-500 mb-2">Image should be below 4 MB</p>
                  <div className="flex space-x-2">
                    <label className="bg-orange-500 text-white px-3 py-1 rounded text-sm cursor-pointer hover:bg-orange-600 transition-colors">
                      Upload
                      <input
                        type="file"
                        accept="image/*"
                        onChange={handleImageUpload}
                        className="hidden"
                      />
                    </label>
                    <button
                      type="button"
                      className="border border-gray-300 px-3 py-1 rounded text-sm hover:bg-gray-50 transition-colors"
                      onClick={() => setFormData(prev => ({ ...prev, profileImage: null }))}
                    >
                      Cancel
                    </button>
                  </div>
                </div>
              </div>

              {/* Hierarchy Selection */}
              {(type === 'retailer' || type === 'distributor' || type === 'sub_distributor') && (
                <div className="bg-blue-50 p-4 rounded-lg border border-blue-200">
                  <h3 className="text-sm font-medium text-blue-800 mb-3">
                    Hierarchy Selection
                  </h3>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {/* Super Distributor Selection */}
                    {renderSuperDistributorDropdown()}

                    {/* Distributor Selection - For Sub Distributor and Retailer */}
                    {(type === 'sub_distributor' || type === 'retailer') && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Select Distributor <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <select
                            value={formData.selectedDistributor}
                            onChange={(e) => handleInputChange('selectedDistributor', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none pr-8"
                            disabled={!formData.selectedSuperDistributor}
                            required
                          >
                            <option value="">Choose Distributor</option>
                            {getFilteredDistributors().map((dist) => (
                              <option key={dist.id} value={dist.id}>
                                {dist.code} - {dist.name}
                              </option>
                            ))}
                          </select>
                          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={16} />
                        </div>
                        {!formData.selectedSuperDistributor && (
                          <p className="text-xs text-gray-500 mt-1">Please select a Super Distributor first</p>
                        )}
                      </div>
                    )}

                    {/* Sub Distributor Selection - Only for Retailer */}
                    {type === 'retailer' && (
                      <div>
                        <label className="block text-sm font-medium text-gray-700 mb-1">
                          Select Sub Distributor <span className="text-red-500">*</span>
                        </label>
                        <div className="relative">
                          <select
                            value={formData.selectedSubDistributor}
                            onChange={(e) => handleInputChange('selectedSubDistributor', e.target.value)}
                            className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent appearance-none pr-8"
                            disabled={!formData.selectedDistributor}
                            required
                          >
                            <option value="">Choose Sub Distributor</option>
                            {getFilteredSubDistributors().map((sub) => (
                              <option key={sub.id} value={sub.id}>
                                {sub.code} - {sub.name}
                              </option>
                            ))}
                          </select>
                          <ChevronDown className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 pointer-events-none" size={16} />
                        </div>
                        {!formData.selectedDistributor && (
                          <p className="text-xs text-gray-500 mt-1">Please select a Distributor first</p>
                        )}
                      </div>
                    )}
                  </div>
                </div>
              )}

              {/* Personal Information Fields */}
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    First Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.firstName}
                    onChange={(e) => handleInputChange('firstName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter first name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Last Name
                  </label>
                  <input
                    type="text"
                    value={formData.lastName}
                    onChange={(e) => handleInputChange('lastName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter last name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Email <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="email"
                    value={formData.email}
                    onChange={(e) => handleInputChange('email', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter email address"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Phone Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    value={formData.phoneNumber}
                    onChange={(e) => handleInputChange('phoneNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter 10-digit phone number"
                    required
                  />
                  {formData.phoneNumber && formData.phoneNumber.length > 0 && formData.phoneNumber.length !== 10 && (
                    <p className="text-xs text-red-500 mt-1">Phone number must be exactly 10 digits</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Date of Birth
                  </label>
                  <input
                    type="date"
                    value={formData.dateOfBirth}
                    onChange={(e) => handleInputChange('dateOfBirth', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Anniversary Date
                  </label>
                  <input
                    type="date"
                    value={formData.anniversaryDate}
                    onChange={(e) => handleInputChange('anniversaryDate', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  />
                </div>

                {/* Password fields - only show in add mode */}
                {!isEdit && (
                  <>
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Password <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type={showPassword ? "text" : "password"}
                          value={formData.password}
                          onChange={(e) => handleInputChange('password', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent pr-10"
                          placeholder="Enter password"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowPassword(!showPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          {showPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Confirm Password <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type={showConfirmPassword ? "text" : "password"}
                          value={formData.confirmPassword}
                          onChange={(e) => handleInputChange('confirmPassword', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent pr-10"
                          placeholder="Confirm password"
                          required
                        />
                        <button
                          type="button"
                          onClick={() => setShowConfirmPassword(!showConfirmPassword)}
                          className="absolute right-3 top-1/2 transform -translate-y-1/2 text-gray-400 hover:text-gray-600"
                        >
                          {showConfirmPassword ? <EyeOff size={16} /> : <Eye size={16} />}
                        </button>
                      </div>
                      {formData.password && formData.confirmPassword && formData.password !== formData.confirmPassword && (
                        <p className="text-xs text-red-500 mt-1">Passwords do not match</p>
                      )}
                    </div>
                  </>
                )}
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  About
                </label>
                <textarea
                  value={formData.about}
                  onChange={(e) => handleInputChange('about', e.target.value)}
                  rows="4"
                  className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  placeholder="Tell us about yourself..."
                />
              </div>
            </div>
          )}

          {/* Business Details Tab */}
          {activeTab === 'business' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.businessName}
                    onChange={(e) => handleInputChange('businessName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter business name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Type <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={formData.businessType}
                    onChange={(e) => handleInputChange('businessType', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select Business Type</option>
                    <option value="Sole Proprietorship">Sole Proprietorship</option>
                    <option value="Partnership">Partnership</option>
                    <option value="Private Limited">Private Limited</option>
                    <option value="LLP">Limited Liability Partnership</option>
                    <option value="Public Limited">Public Limited</option>
                  </select>
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    GST Number
                  </label>
                  <input
                    type="text"
                    value={formData.gstNumber}
                    onChange={(e) => handleInputChange('gstNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="27AAPFU0939F1ZV"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    PAN Number
                  </label>
                  <input
                    type="text"
                    value={formData.panNumber}
                    onChange={(e) => handleInputChange('panNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="AAPFU0939F"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Registration Number
                  </label>
                  <input
                    type="text"
                    value={formData.businessRegistrationNumber}
                    onChange={(e) => handleInputChange('businessRegistrationNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter registration number"
                  />
                </div>
              </div>
            </div>
          )}

          {/* Address Details Tab */}
          {activeTab === 'address' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                {/* Address Form */}
                <div className="space-y-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Business Address <span className="text-red-500">*</span>
                    </label>
                    <textarea
                      value={formData.businessAddress}
                      onChange={(e) => handleInputChange('businessAddress', e.target.value)}
                      rows="3"
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                      placeholder="Enter complete business address"
                      required
                    />
                  </div>

                  <div className="grid grid-cols-2 gap-4">
                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        Pincode <span className="text-red-500">*</span>
                      </label>
                      <div className="relative">
                        <input
                          type="text"
                          value={formData.businessPincode}
                          onChange={(e) => handleInputChange('businessPincode', e.target.value)}
                          className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent pr-10"
                          placeholder="Enter 6-digit pincode"
                          required
                        />
                        {isLoadingAddress && (
                          <Loader className="absolute right-3 top-1/2 transform -translate-y-1/2 text-orange-500 animate-spin" size={16} />
                        )}
                      </div>
                      {formData.businessPincode && formData.businessPincode.length > 0 && formData.businessPincode.length !== 6 && (
                        <p className="text-xs text-red-500 mt-1">Pincode must be exactly 6 digits</p>
                      )}
                    </div>

                    <div>
                      <label className="block text-sm font-medium text-gray-700 mb-1">
                        City <span className="text-red-500">*</span>
                      </label>
                      <input
                        type="text"
                        value={formData.businessCity}
                        onChange={(e) => handleInputChange('businessCity', e.target.value)}
                        className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                        placeholder="Auto-filled from pincode"
                        required
                        readOnly
                      />
                    </div>
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      State <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.businessState}
                      onChange={(e) => handleInputChange('businessState', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent bg-gray-50"
                      placeholder="Auto-filled from pincode"
                      required
                      readOnly
                    />
                  </div>

                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-1">
                      Landmarks <span className="text-red-500">*</span>
                    </label>
                    <input
                      type="text"
                      value={formData.landmarks}
                      onChange={(e) => handleInputChange('landmarks', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                      placeholder="e.g., Near City Mall, Opposite Bank"
                      required
                    />
                  </div>
                </div>

                {/* Map View */}
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Location on Map <span className="text-red-500">*</span>
                  </label>
                  <MapView />
                </div>
              </div>
            </div>
          )}

          {/* Contact Details Tab */}
          {activeTab === 'contact' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Alternate Phone Number
                  </label>
                  <input
                    type="tel"
                    value={formData.alternatePhoneNumber}
                    onChange={(e) => handleInputChange('alternatePhoneNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter alternate phone number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    WhatsApp Number
                  </label>
                  <input
                    type="tel"
                    value={formData.whatsappNumber}
                    onChange={(e) => handleInputChange('whatsappNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter WhatsApp number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Phone Number
                  </label>
                  <input
                    type="tel"
                    value={formData.businessPhoneNumber}
                    onChange={(e) => handleInputChange('businessPhoneNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter business phone number"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Business Email
                  </label>
                  <input
                    type="email"
                    value={formData.businessEmail}
                    onChange={(e) => handleInputChange('businessEmail', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter business email"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Contact Person Name
                  </label>
                  <input
                    type="text"
                    value={formData.contactPersonName}
                    onChange={(e) => handleInputChange('contactPersonName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter contact person name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Contact Person Designation
                  </label>
                  <input
                    type="text"
                    value={formData.contactPersonDesignation}
                    onChange={(e) => handleInputChange('contactPersonDesignation', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter designation"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Emergency Contact Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.emergencyContactName}
                    onChange={(e) => handleInputChange('emergencyContactName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter emergency contact name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Emergency Contact Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="tel"
                    value={formData.emergencyContactNumber}
                    onChange={(e) => handleInputChange('emergencyContactNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter emergency contact number"
                    required
                  />
                  {formData.emergencyContactNumber && formData.emergencyContactNumber.length > 0 && formData.emergencyContactNumber.length !== 10 && (
                    <p className="text-xs text-red-500 mt-1">Phone number must be exactly 10 digits</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Emergency Contact Relation <span className="text-red-500">*</span>
                  </label>
                  <select
                    value={formData.emergencyContactRelation}
                    onChange={(e) => handleInputChange('emergencyContactRelation', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    required
                  >
                    <option value="">Select Relation</option>
                    <option value="Father">Father</option>
                    <option value="Mother">Mother</option>
                    <option value="Spouse">Spouse</option>
                    <option value="Brother">Brother</option>
                    <option value="Sister">Sister</option>
                    <option value="Friend">Friend</option>
                    <option value="Business Partner">Business Partner</option>
                    <option value="Other">Other</option>
                  </select>
                </div>
              </div>
            </div>
          )}

          {/* Documents Tab */}
          {activeTab === 'documents' && (
            <div className="space-y-6">
              <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-orange-400 transition-colors">
                <Upload className="mx-auto h-12 w-12 text-gray-400 mb-4" />
                <h3 className="text-lg font-medium text-gray-900 mb-2">Upload Documents</h3>
                <p className="text-sm text-gray-500 mb-4">
                  Upload GST certificate, PAN card, business registration, bank statements, and other relevant documents
                </p>
                <p className="text-xs text-gray-400 mb-4">
                  Supported formats: PDF, DOC, DOCX, JPG, PNG (Max size: 4MB each)
                </p>
                <label className="bg-orange-500 text-white px-6 py-2 rounded-lg cursor-pointer hover:bg-orange-600 inline-flex items-center gap-2 transition-colors">
                  <Upload size={16} />
                  Choose Files
                  <input
                    type="file"
                    multiple
                    accept=".pdf,.doc,.docx,.jpg,.jpeg,.png"
                    onChange={handleDocumentUpload}
                    className="hidden"
                  />
                </label>
              </div>

              {/* Uploaded Documents List */}
              {formData.documents.length > 0 && (
                <div className="space-y-3">
                  <h4 className="font-medium text-gray-900">
                    {isEdit ? 'Documents' : 'Uploaded Documents'} ({formData.documents.length})
                  </h4>
                  {formData.documents.map((doc) => (
                    <div key={doc.id} className="flex items-center justify-between p-3 border border-gray-200 rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors">
                      <div className="flex items-center space-x-3">
                        <FileText className="h-8 w-8 text-orange-500" />
                        <div>
                          <p className="text-sm font-medium text-gray-900">{doc.name}</p>
                          <div className="flex items-center space-x-2">
                            <p className="text-xs text-gray-500">{formatFileSize(doc.size)}</p>
                            {doc.isExisting && (
                              <span className="text-xs bg-blue-100 text-blue-800 px-2 py-0.5 rounded-full">
                                Existing
                              </span>
                            )}
                          </div>
                        </div>
                      </div>
                      <button
                        onClick={() => removeDocument(doc.id)}
                        className="text-red-500 hover:text-red-700 p-1 rounded-full hover:bg-red-50 transition-colors"
                        title="Remove document"
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}

          {/* Banking Details Tab */}
          {activeTab === 'banking' && (
            <div className="space-y-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Bank Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.bankName}
                    onChange={(e) => handleInputChange('bankName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter bank name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Account Number <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.accountNumber}
                    onChange={(e) => handleInputChange('accountNumber', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter account number"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    IFSC Code <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.ifscCode}
                    onChange={(e) => handleInputChange('ifscCode', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="SBIN0001234"
                    required
                  />
                  {formData.ifscCode && formData.ifscCode.length > 0 && formData.ifscCode.length !== 11 && (
                    <p className="text-xs text-red-500 mt-1">IFSC code must be exactly 11 characters</p>
                  )}
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Account Holder Name <span className="text-red-500">*</span>
                  </label>
                  <input
                    type="text"
                    value={formData.accountHolderName}
                    onChange={(e) => handleInputChange('accountHolderName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter account holder name"
                    required
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Branch Name
                  </label>
                  <input
                    type="text"
                    value={formData.branchName}
                    onChange={(e) => handleInputChange('branchName', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                    placeholder="Enter branch name"
                  />
                </div>

                <div>
                  <label className="block text-sm font-medium text-gray-700 mb-1">
                    Account Type
                  </label>
                  <select
                    value={formData.accountType}
                    onChange={(e) => handleInputChange('accountType', e.target.value)}
                    className="w-full px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-orange-500 focus:border-transparent"
                  >
                    <option value="">Select Account Type</option>
                    <option value="Savings">Savings Account</option>
                    <option value="Current">Current Account</option>
                    <option value="Business">Business Account</option>
                  </select>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="border-t border-gray-200 px-6 py-4 bg-gray-50">
          <div className="flex justify-between items-center">
            <div>
              {activeTab !== 'basic' && (
                <button
                  type="button"
                  onClick={goToPreviousTab}
                  className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
                >
                  Previous
                </button>
              )}
            </div>
            
            <div className="flex items-center space-x-3">
              <button
                type="button"
                onClick={onClose}
                className="px-4 py-2 border border-gray-300 rounded-lg text-gray-700 hover:bg-gray-50 transition-colors"
              >
                Cancel
              </button>
              
              {activeTab !== 'banking' ? (
                <button
                  type="button"
                  disabled={!completedSections[activeTab]}
                  onClick={goToNextTab}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    completedSections[activeTab]
                      ? 'bg-orange-500 text-white hover:bg-orange-600' 
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  Next
                </button>
              ) : (
                <button
                  type="submit"
                  onClick={handleSubmit}
                  disabled={!completedSections.banking}
                  className={`px-4 py-2 rounded-lg transition-colors ${
                    completedSections.banking
                      ? 'bg-green-500 text-white hover:bg-green-600'
                      : 'bg-gray-300 text-gray-500 cursor-not-allowed'
                  }`}
                >
                  {modalConfig.buttonText}
                </button>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AddDistributorModal;
