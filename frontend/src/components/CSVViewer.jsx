import React, { useState, useEffect } from 'react';
import { ChevronDown, ChevronUp, Download } from 'lucide-react';
import Papa from 'papaparse';

const formatMetrics = (metricsString) => {
  try {
    const metrics = JSON.parse(metricsString);
    return (
      <div className="space-y-2">
        {Object.entries(metrics).map(([key, value]) => {
          if (typeof value === 'object' && value !== null) {
            return (
              <div key={key} className="pl-2 border-l-2 border-gray-200">
                <span className="font-medium">{key.replace(/_/g, ' ')}:</span>
                <div className="pl-3 text-sm">
                  {Object.entries(value).map(([subKey, subValue]) => (
                    <div key={subKey}>
                      <span className="text-gray-600">{subKey.replace(/_/g, ' ')}: </span>
                      <span>{subValue}</span>
                    </div>
                  ))}
                </div>
              </div>
            );
          }
          return (
            <div key={key}>
              <span className="font-medium">{key.replace(/_/g, ' ')}: </span>
              <span>{value}</span>
            </div>
          );
        })}
      </div>
    );
  } catch (e) {
    return metricsString;
  }
};

const formatKeyFindings = (findings) => {
  if (!findings) return null;
  const findingsList = findings.split(';').filter(finding => finding.trim());
  return (
    <ul className="list-disc pl-4 space-y-1">
      {findingsList.map((finding, index) => (
        <li key={index} className="text-sm">{finding.trim()}</li>
      ))}
    </ul>
  );
};

const formatSources = (sources) => {
  if (!sources) return null;
  const sourcesList = sources.split(';').filter(source => source.trim());
  return (
    <ul className="list-none space-y-1 text-sm">
      {sourcesList.map((source, index) => (
        <li key={index} className="text-gray-600">{source.trim()}</li>
      ))}
    </ul>
  );
};

const ExpandableText = ({ content, defaultExpanded = false }) => {
  const [isExpanded, setIsExpanded] = useState(defaultExpanded);
  const previewLength = 100;
  const needsExpansion = content?.length > previewLength;

  if (!needsExpansion) return <div className="text-sm">{content}</div>;

  return (
    <div className="relative">
      <div className="text-sm">
        {isExpanded ? content : `${content.slice(0, previewLength)}...`}
        <button
          onClick={() => setIsExpanded(!isExpanded)}
          className="ml-2 text-blue-500 hover:text-blue-700 inline-flex items-center"
        >
          {isExpanded ? (
            <>Show less <ChevronUp className="w-4 h-4 ml-1" /></>
          ) : (
            <>Show more <ChevronDown className="w-4 h-4 ml-1" /></>
          )}
        </button>
      </div>
    </div>
  );
};

const DataCell = ({ content, type }) => {
  switch (type) {
    case 'Metrics':
      return formatMetrics(content);
    case 'Key Findings':
      return formatKeyFindings(content);
    case 'Sources':
      return formatSources(content);
    default:
      return <ExpandableText content={content} />;
  }
};

const CSVViewer = ({ initialData }) => {
  const [parsedData, setParsedData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  useEffect(() => {
    if (initialData) {
      fetchAndParseData(initialData);
    }
  }, [initialData]);

  const fetchAndParseData = async (data) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch('http://localhost:8000/api/analyze', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(data)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const result = await response.json();
      
      // Use Papa Parse to properly parse the CSV data
      Papa.parse(result.data, {
        header: true,
        complete: (results) => {
          setParsedData(results.data);
        },
        error: (error) => {
          setError(`CSV parsing error: ${error}`);
        }
      });
    } catch (err) {
      setError(err.message);
      console.error('Error fetching data:', err);
    } finally {
      setLoading(false);
    }
  };

  const downloadCSV = () => {
    if (!parsedData) return;
    
    const csv = Papa.unparse(parsedData);
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
    const url = URL.createObjectURL(blob);
    const link = document.createElement('a');
    
    link.setAttribute('href', url);
    link.setAttribute('download', 'analysis_results.csv');
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center p-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-500"></div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="text-red-500 mb-4 p-4 bg-red-50 rounded-lg">
        Error: {error}
      </div>
    );
  }

  if (!parsedData) {
    return null;
  }

  const headers = Object.keys(parsedData[0] || {});

  return (
    <div className="w-full max-w-6xl bg-white rounded-lg shadow-lg overflow-hidden">
      <div className="p-6 border-b border-gray-200">
        <div className="flex justify-between items-center">
          <h2 className="text-xl font-semibold text-gray-800">Analysis Results</h2>
          <button
            onClick={downloadCSV}
            className="flex items-center px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition-colors"
          >
            <Download className="w-4 h-4 mr-2" />
            Download CSV
          </button>
        </div>
      </div>

      <div className="p-6 overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {headers.map((header) => (
                <th
                  key={header}
                  className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider"
                >
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {parsedData.map((row, rowIndex) => (
              <tr 
                key={rowIndex}
                className="hover:bg-gray-50 transition-colors"
              >
                {headers.map((header) => (
                  <td
                    key={`${rowIndex}-${header}`}
                    className="px-6 py-4"
                  >
                    <DataCell 
                      content={row[header]} 
                      type={header}
                    />
                  </td>
                ))}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default CSVViewer;