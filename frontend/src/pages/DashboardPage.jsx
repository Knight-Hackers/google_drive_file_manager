import React, { useState, useEffect } from 'react';
import { 
  Briefcase, GraduationCap, Music, Camera, FolderOpen, 
  Utensils, Heart, Dumbbell, Book, Code, ShoppingBag,
  Plane, Home, DollarSign, FileText, ChevronDown, ChevronUp,
  Sparkles, Filter, X
} from 'lucide-react';

const DriveDashboard = () => {
  const [driveData, setDriveData] = useState(null);
  const [expandedCategory, setExpandedCategory] = useState(null);
  const [categorizationMethod, setCategorizationMethod] = useState('heuristic');
  const [isLoading, setIsLoading] = useState(false);

  const iconMap = {
    school: GraduationCap,
    work: Briefcase,
    cooking: Utensils,
    photos: Camera,
    music: Music,
    personal: Heart,
    fitness: Dumbbell,
    books: Book,
    code: Code,
    shopping: ShoppingBag,
    travel: Plane,
    home: Home,
    finance: DollarSign,
    other: FolderOpen,
  };

  const colorSchemes = [
    { border: '#60a5fa', bg: '#eff6ff', text: '#1e40af' },
    { border: '#f87171', bg: '#fef2f2', text: '#991b1b' },
    { border: '#fbbf24', bg: '#fffbeb', text: '#92400e' },
    { border: '#34d399', bg: '#f0fdf4', text: '#065f46' },
    { border: '#a78bfa', bg: '#f5f3ff', text: '#5b21b6' },
    { border: '#f472b6', bg: '#fdf2f8', text: '#9f1239' },
    { border: '#818cf8', bg: '#eef2ff', text: '#3730a3' },
    { border: '#fb923c', bg: '#fff7ed', text: '#9a3412' },
    { border: '#2dd4bf', bg: '#f0fdfa', text: '#115e59' },
    { border: '#22d3ee', bg: '#ecfeff', text: '#155e75' },
  ];

  const getIconForCategory = (category) => {
    const categoryLower = category.toLowerCase().replace(/\s+/g, '');
    if (iconMap[categoryLower]) {
      return iconMap[categoryLower];
    }
    return FolderOpen;
  };

  const getColorForCategory = (index) => {
    return colorSchemes[index % colorSchemes.length];
  };

  const token = localStorage.getItem('access_token');
// Fetch data based on categorization method
  const fetchDriveData = async (method) => {
    setIsLoading(true);
    try {
      // Replace with your actual API endpoint
      const endpoint = method === 'heuristic' 
        ? '/files/analyze/heuristic' 
        : '/files/analyze/gemini';
      
      const response = await fetch(`http://localhost:8000${endpoint}`, {
        method: 'POST',
        headers: { Authorization: `Bearer ${token}`}
      }

      );
      const data = await response.json();
      setDriveData(data);
    } catch (error) {
      console.error('Error fetching drive data:', error);
      // Fallback to sample data for demo
      setDriveData(getSampleData(method));
    } finally {
      setIsLoading(false);
    }
  };

  const getSampleData = (method) => {
    if (method === 'heuristic') {
      return {
        total_files: 487,
        categories: {
          work: 124,
          personal: 89,
          photos: 156,
          documents: 78,
          other: 40
        },
        files: [
          {name: "Q4 Report.docx", category: "work", size: "2.3 MB", modified: "2025-10-20"},
          {name: "Resume 2025.pdf", category: "work", size: "156 KB", modified: "2025-10-18"},
          {name: "Budget Planning.xlsx", category: "work", size: "890 KB", modified: "2025-10-15"},
          {name: "Birthday Photos.zip", category: "photos", size: "45 MB", modified: "2025-10-10"},
          {name: "Vacation 2025.jpg", category: "photos", size: "3.2 MB", modified: "2025-10-08"},
          {name: "Family Reunion.jpg", category: "photos", size: "2.8 MB", modified: "2025-10-05"},
          {name: "Tax Documents 2024.pdf", category: "documents", size: "1.1 MB", modified: "2025-09-30"},
          {name: "Insurance Policy.pdf", category: "documents", size: "567 KB", modified: "2025-09-28"},
          {name: "Personal Notes.txt", category: "personal", size: "12 KB", modified: "2025-10-22"},
          {name: "Reading List.docx", category: "personal", size: "34 KB", modified: "2025-10-19"},
          {name: "Random Files.zip", category: "other", size: "15 MB", modified: "2025-10-12"},
        ]
      };
    } else {
      return {
        total_files: 9,
        categories: {
          "Personal Development": 3,
          "Job Applications": 2,
          "Exam Material": 1,
          "Personal Finance": 1,
          "Schoolwork": 2
        },
        files: [
          {name: "Journal entry 1", category: "Personal Development"},
          {name: "Motivation", category: "Personal Development"},
          {name: "Siemens cover letter", category: "Job Applications"},
          {name: "Trivago cover letter", category: "Job Applications"},
          {name: "Journal entry", category: "Personal Development"},
          {name: "Exam notes", category: "Exam Material"},
          {name: "Taxes", category: "Personal Finance"},
          {name: "science homework", category: "Schoolwork"},
          {name: "Math homework", category: "Schoolwork"}
        ]
      };
    }
  };

  useEffect(() => {
    fetchDriveData(categorizationMethod);
  }, []);

  const handleMethodChange = (method) => {
    setCategorizationMethod(method);
    setExpandedCategory(null);
    fetchDriveData(method);
  };

  const toggleCategory = (category) => {
    setExpandedCategory(expandedCategory === category ? null : category);
  };

  const getFilesForCategory = (category) => {
    if (!driveData) return [];
    return driveData.files.filter(file => file.category === category);
  };

  if (!driveData) {
    return (
      <div style={{ 
        minHeight: '100vh', 
        backgroundColor: '#f9fafb',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center'
      }}>
        <div style={{ textAlign: 'center' }}>
          <div style={{
            width: '48px',
            height: '48px',
            border: '3px solid #e5e7eb',
            borderTopColor: '#2563eb',
            borderRadius: '50%',
            animation: 'spin 1s linear infinite',
            margin: '0 auto 16px'
          }}></div>
          <p style={{ color: '#4b5563', margin: 0 }}>Loading your drive...</p>
        </div>
      </div>
    );
  }
  console.log(driveData);
  const totalCategories = Object.keys(driveData.categories).length;

  return (
    <div style={{ 
      minHeight: '100vh', 
      backgroundColor: '#f9fafb',
      padding: '32px 16px',
      color: '#111827'
    }}>
      <div style={{ maxWidth: '1280px', margin: '0 auto' }}>
        {/* Header */}
        <div style={{ 
          display: 'flex', 
          alignItems: 'center', 
          justifyContent: 'space-between',
          marginBottom: '32px',
          flexWrap: 'wrap',
          gap: '16px'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
            <div style={{ display: 'flex', gap: '8px' }}>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#ef4444' }}></div>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#eab308' }}></div>
              <div style={{ width: '12px', height: '12px', borderRadius: '50%', backgroundColor: '#22c55e' }}></div>
            </div>
            <h1 style={{ 
              fontSize: '30px', 
              fontWeight: 600, 
              color: '#1f2937',
              margin: 0,
              lineHeight: 1.2
            }}>My Drive</h1>
          </div>
          
          {/* Categorization Method Toggle */}
          <div style={{ 
            display: 'flex', 
            gap: '8px', 
            backgroundColor: 'white',
            borderRadius: '12px',
            padding: '4px',
            boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
            border: '1px solid #e5e7eb'
          }}>
            <button
              onClick={() => handleMethodChange('heuristic')}
              disabled={isLoading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 16px',
                borderRadius: '8px',
                border: 'none',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s',
                backgroundColor: categorizationMethod === 'heuristic' ? '#2563eb' : 'transparent',
                color: categorizationMethod === 'heuristic' ? 'white' : '#4b5563',
                fontSize: '14px',
                fontWeight: 500,
                opacity: isLoading ? 0.5 : 1
              }}
            >
              <Filter size={16} />
              <span>Heuristic</span>
            </button>
            <button
              onClick={() => handleMethodChange('ai')}
              disabled={isLoading}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 16px',
                borderRadius: '8px',
                border: 'none',
                cursor: isLoading ? 'not-allowed' : 'pointer',
                transition: 'all 0.2s',
                backgroundColor: categorizationMethod === 'ai' ? '#7c3aed' : 'transparent',
                color: categorizationMethod === 'ai' ? 'white' : '#4b5563',
                fontSize: '14px',
                fontWeight: 500,
                opacity: isLoading ? 0.5 : 1
              }}
            >
              <Sparkles size={16} />
              <span>AI-Powered</span>
            </button>
          </div>
        </div>

        {/* Method Description */}
        <div style={{
          backgroundColor: '#dbeafe',
          border: '1px solid #93c5fd',
          borderRadius: '12px',
          padding: '16px',
          marginBottom: '32px'
        }}>
          <p style={{ fontSize: '14px', color: '#1e40af', margin: 0 }}>
            {categorizationMethod === 'heuristic' ? (
              <>
                <strong>Heuristic Mode:</strong> Files are categorized using keyword matching from document titles.
              </>
            ) : (
              <>
                <strong>AI-Powered Mode:</strong> Gemini analyzes file content and creates intelligent, contextual categories.
              </>
            )}
          </p>
        </div>

        {/* Quick Stats Summary */}
        <div style={{
          backgroundColor: 'white',
          borderRadius: '24px',
          boxShadow: '0 1px 3px rgba(0,0,0,0.1)',
          padding: '24px',
          marginBottom: '32px',
          border: '1px solid #e5e7eb'
        }}>
          <div style={{ 
            display: 'flex', 
            alignItems: 'center', 
            justifyContent: 'space-around',
            flexWrap: 'wrap',
            gap: '24px'
          }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '42px', fontWeight: 700, color: '#2563eb' }}>
                {driveData.total_files}
              </div>
              <div style={{ color: '#6b7280', marginTop: '4px' }}>Total Files</div>
            </div>
            <div style={{ height: '64px', width: '1px', backgroundColor: '#d1d5db' }}></div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '42px', fontWeight: 700, color: '#059669' }}>
                {totalCategories}
              </div>
              <div style={{ color: '#6b7280', marginTop: '4px' }}>Categories</div>
            </div>
          </div>
        </div>

        {/* Loading Overlay */}
        {isLoading && (
          <div style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(0,0,0,0.3)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 50
          }}>
            <div style={{
              backgroundColor: 'white',
              borderRadius: '12px',
              padding: '24px',
              boxShadow: '0 10px 25px rgba(0,0,0,0.2)',
              textAlign: 'center'
            }}>
              <div style={{
                width: '48px',
                height: '48px',
                border: '3px solid #e5e7eb',
                borderTopColor: '#2563eb',
                borderRadius: '50%',
                animation: 'spin 1s linear infinite',
                margin: '0 auto 16px'
              }}></div>
              <p style={{ color: '#374151', margin: 0 }}>Recategorizing files...</p>
            </div>
          </div>
        )}

        {/* Category Cards Grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
          gap: '24px'
        }}>
          {Object.entries(driveData.categories).map(([category, count], index) => {
            const Icon = getIconForCategory(category);
            const colors = getColorForCategory(index);
            const isExpanded = expandedCategory === category;
            const categoryFiles = getFilesForCategory(category);
            
            return (
              <div key={category} style={{ transition: 'all 0.3s' }}>
                {/* Category Card */}
                <div
                  onClick={() => toggleCategory(category)}
                  style={{
                    border: `3px solid ${colors.border}`,
                    backgroundColor: colors.bg,
                    borderRadius: '24px',
                    padding: '32px',
                    cursor: 'pointer',
                    transition: 'all 0.3s',
                    transform: isExpanded ? 'scale(1.02)' : 'scale(1)',
                    boxShadow: isExpanded ? '0 10px 25px rgba(0,0,0,0.1)' : '0 1px 3px rgba(0,0,0,0.05)'
                  }}
                  onMouseEnter={(e) => {
                    if (!isExpanded) e.currentTarget.style.transform = 'scale(1.02)';
                    e.currentTarget.style.boxShadow = '0 10px 25px rgba(0,0,0,0.1)';
                  }}
                  onMouseLeave={(e) => {
                    if (!isExpanded) e.currentTarget.style.transform = 'scale(1)';
                    if (!isExpanded) e.currentTarget.style.boxShadow = '0 1px 3px rgba(0,0,0,0.05)';
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'flex-start', justifyContent: 'space-between' }}>
                    <div style={{ flex: 1 }}>
                      <Icon size={48} color={colors.text} strokeWidth={1.5} style={{ marginBottom: '16px' }} />
                      <h2 style={{
                        fontSize: '24px',
                        fontWeight: 600,
                        color: '#1f2937',
                        marginBottom: '8px',
                        marginTop: 0
                      }}>
                        {category}
                      </h2>
                      <p style={{ color: '#6b7280', fontSize: '18px', margin: 0 }}>
                        {count} {count === 1 ? 'file' : 'files'}
                      </p>
                    </div>
                    <div style={{ marginLeft: '16px' }}>
                      {isExpanded ? (
                        <ChevronUp size={24} color="#4b5563" />
                      ) : (
                        <ChevronDown size={24} color="#4b5563" />
                      )}
                    </div>
                  </div>
                </div>

                {/* Expanded Files List */}
                {isExpanded && (
                  <div style={{
                    marginTop: '16px',
                    backgroundColor: 'white',
                    borderRadius: '24px',
                    boxShadow: '0 4px 12px rgba(0,0,0,0.1)',
                    border: '1px solid #e5e7eb',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      padding: '16px',
                      backgroundColor: '#f9fafb',
                      borderBottom: '1px solid #e5e7eb',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between'
                    }}>
                      <h3 style={{ fontWeight: 600, color: '#1f2937', margin: 0 }}>
                        Files in {category}
                      </h3>
                      <button
                        onClick={(e) => {
                          e.stopPropagation();
                          setExpandedCategory(null);
                        }}
                        style={{
                          background: 'none',
                          border: 'none',
                          cursor: 'pointer',
                          padding: '4px',
                          display: 'flex',
                          alignItems: 'center',
                          color: '#6b7280'
                        }}
                      >
                        <X size={20} />
                      </button>
                    </div>
                    <div style={{ maxHeight: '384px', overflowY: 'auto' }}>
                      {categoryFiles.length > 0 ? (
                        <div>
                          {categoryFiles.map((file, idx) => (
                            <div
                              key={idx}
                              style={{
                                padding: '16px',
                                borderBottom: idx < categoryFiles.length - 1 ? '1px solid #f3f4f6' : 'none',
                                transition: 'background-color 0.2s'
                              }}
                              onMouseEnter={(e) => e.currentTarget.style.backgroundColor = '#f9fafb'}
                              onMouseLeave={(e) => e.currentTarget.style.backgroundColor = 'transparent'}
                            >
                              <div style={{
                                display: 'flex',
                                alignItems: 'center',
                                justifyContent: 'space-between'
                              }}>
                                <div style={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: '12px',
                                  flex: 1,
                                  minWidth: 0
                                }}>
                                  <FileText size={20} color="#6b7280" style={{ flexShrink: 0 }} />
                                  <div style={{ minWidth: 0, flex: 1 }}>
                                    <p style={{
                                      color: '#1f2937',
                                      fontWeight: 500,
                                      margin: 0,
                                      marginBottom: '2px',
                                      overflow: 'hidden',
                                      textOverflow: 'ellipsis',
                                      whiteSpace: 'nowrap'
                                    }}>
                                      {file.name}
                                    </p>
                                    <p style={{
                                      fontSize: '14px',
                                      color: '#6b7280',
                                      margin: 0
                                    }}>
                                      {/*{file.size} • Modified {file.modified}*/}
                                    </p>
                                  </div>
                                </div>
                              </div>
                            </div>
                          ))}
                        </div>
                      ) : (
                        <div style={{
                          padding: '64px 32px',
                          textAlign: 'center',
                          color: '#6b7280'
                        }}>
                          No files found in this category
                        </div>
                      )}
                    </div>
                  </div>
                )}
              </div>
            );
          })}
        </div>
      </div>

      <style>{`
        @keyframes spin {
          to { transform: rotate(360deg); }
        }
      `}</style>
    </div>
  );
};

export default DriveDashboard;