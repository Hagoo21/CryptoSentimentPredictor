import React, { useState, useEffect } from 'react';

const RPMGauge = ({ value, reset }) => {
  const [rotationAngle, setRotationAngle] = useState(-90); // Start at 12 o'clock position (-90 degrees)
  const gaugeSize = 400;

  useEffect(() => {
    // Reset rotation angle when reset prop changes
    if (reset) {
      setRotationAngle(-90);
    }
  }, [reset]);

  useEffect(() => {
    // Calculate new rotation angle based on value
    const newRotationAngle = (value < 0.5 ? -60 : 60); // -60 for red half, 60 for green half
    setRotationAngle(newRotationAngle);
  }, [value]);

  return (
    <div style={{ width: gaugeSize, height: gaugeSize / 2, position: 'relative', margin: '40px 20px', overflow: 'hidden' }}>
      {/* RPM Gauge Arc */}
      <div
        style={{
          position: 'absolute',
          top: '100%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: '100%',
          height: gaugeSize,
          borderRadius: '50%',
          background: 'linear-gradient(to right, green 50%, red 50%)', // Switched colors
          border: '10px solid #ccc',
          borderBottom: '10px solid grey',
          boxSizing: 'border-box',
        }}
      />

      {/* RPM Gauge Needle */}
      <div
        style={{
          position: 'absolute',
          top: '100%',
          left: '50%',
          transform: `translate(-50%, -100%) rotate(${rotationAngle}deg)`,
          width: '50%',
          height: '5px',
          background: 'black',
          borderRadius: '5px',
          zIndex: '1',
          transition: 'transform 0.5s ease',
        }}
      />

      {/* Labels */}
      <div
        style={{
          position: 'absolute',
          bottom: '10px',
          left: '10px',
          fontSize: '14px',
          fontWeight: 'bold',
          color: 'black',
        }}
      >
        0
      </div>
      <div
        style={{
          position: 'absolute',
          bottom: '10px',
          right: '10px',
          fontSize: '14px',
          fontWeight: 'bold',
          color: 'black',
        }}
      >
        1
      </div>
    </div>
  );
};

const ComponentName = () => {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResult, setSearchResult] = useState(null);
  const [displayedSearchQuery, setDisplayedSearchQuery] = useState('');
  const [resetRotation, setResetRotation] = useState(false);

  const options = ['pepe', 'neuron', 'titan swap', 'shiba inu', 'bert', 'perl'];

  const handleSearch = () => {
    const randomValue = Math.random();
    setSearchResult(randomValue);
    setDisplayedSearchQuery(searchQuery);
    setResetRotation(true); // Trigger rotation reset
  };

  // Filter options based on input
  const filteredOptions = options.filter(option =>
    option.toLowerCase().includes(searchQuery.toLowerCase().slice(0, 3))
  );

  // Reset rotation when searchQuery changes
  useEffect(() => {
    setResetRotation(true);
  }, [searchQuery]);

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: '20px', background: '#f0f0f0' }}>
      <p style={{ fontFamily: 'Times New Roman', fontSize: '20px', marginBottom: '10px' }}>Crypto Sentiment Predictor</p>
      <div style={{ position: 'relative', display: 'flex', alignItems: 'center', marginBottom: '10px' }}>
        <input
          type="text"
          list="options"
          placeholder="Search..."
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          style={{
            width: '300px',
            padding: '12px',
            fontSize: '16px',
            border: '1px solid #ccc',
            borderRadius: '5px',
            marginRight: '10px',
            boxShadow: '0px 2px 4px rgba(0, 0, 0, 0.1)', // Add subtle box-shadow on focus
            transition: 'box-shadow 0.3s ease', // Smooth transition on focus
          }}
        />
        <datalist id="options">
          {filteredOptions.map((option, index) => (
            <option key={index} value={option} />
          ))}
        </datalist>
        <button
          onClick={handleSearch}
          style={{
            padding: '12px 20px',
            fontSize: '16px',
            backgroundColor: '#007bff',
            color: 'white',
            border: 'none',
            borderRadius: '5px',
            cursor: 'pointer',
            transition: 'background-color 0.3s ease', // Smooth transition on hover
          }}
        >
          Search
        </button>
      </div>
      {searchResult !== null && (
        <RPMGauge value={searchResult} reset={resetRotation} />
      )}
      <div
        style={{
          position: 'absolute',
          bottom: '10px',
          right: '10px',
          padding: '10px',
          background: '#f0f0f0',
          border: '1px solid #ccc',
          borderRadius: '5px',
          boxShadow: '0px 4px 8px rgba(0, 0, 0, 0.1)', // Add box shadow for depth
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'flex-end',
        }}
      >
        <p style={{ marginBottom: '5px', fontWeight: 'bold', fontSize: '16px' }}>User Input:</p>
        <p style={{ marginBottom: '5px' }}>{displayedSearchQuery}</p>
        {searchResult !== null && <p style={{ marginBottom: '5px', fontWeight: 'bold', fontSize: '16px' }}>Search Result:</p>}
        {searchResult !== null && <p>{searchResult.toFixed(3)}</p>}
      </div>
    </div>
  );
};

export default ComponentName;
