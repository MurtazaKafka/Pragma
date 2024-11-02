import React, { useState, useEffect } from 'react';
import Papa from 'papaparse';
import './table.css';

const CsvTable = () => {
    const [tableData, setTableData] = useState([]);
    const [headers, setHeaders] = useState([]);

    useEffect(() => {
        const fetchCsvData = async () => {
            try {
                // const response = await fetch('https://example.com/api/csv'); // Replace with your API URL
                // const csvText = await response.text();
                const csvText = `
                Column_1,Column_2,Column_3,
                a,b,c
                d,e,f`;

                Papa.parse(csvText, {
                    header: true,
                    skipEmptyLines: true,
                    complete: (results) => {
                        const rows = results.data;
                        setHeaders(Object.keys(rows[0]));
                        setTableData(rows);
                    },
                });
            } catch (error) {
                console.error('Error fetching data:', error);
            }
        };

        fetchCsvData();
    }, []);

    const handleDownload = () => {
        const csv = Papa.unparse(tableData);
        const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' });
        const url = URL.createObjectURL(blob);
        const link = document.createElement('a');
        link.href = url;
        link.setAttribute('download', 'table_data.csv');
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
    };

    return (
        <div id="data-wrapper">
            <div id="csv-options">
                <button id="home">
                    <i className="fa fa-download"></i>
                </button>
                <button id="download-csv" onClick={handleDownload}>
                    <i className="fa fa-home"></i>
                </button>
            </div>
            <div id="csv-wrapper">
                {tableData.length > 0 ? (
                    <table>
                        <thead>
                            <tr>
                                {headers.map((header) => (
                                    <th key={header}>{header}</th>
                                ))}
                            </tr>
                        </thead>
                        <tbody>
                            {tableData.map((row, index) => (
                                <tr key={index}>
                                    {headers.map((header) => (
                                        <td key={header}>{row[header]}</td>
                                    ))}
                                </tr>
                            ))}
                        </tbody>
                    </table>
                ) : (
                    <p>Loading data...</p>
                )}
            </div>
        </div>
    );
};

export default CsvTable;
