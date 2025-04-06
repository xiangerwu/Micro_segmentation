import React, { useEffect, useState } from "react";
import "./HostsTable.css"; 
import IntentTable from "./IntentTable";
import { Heading , Stack } from "@chakra-ui/react";

function HostsTable(){
  const [hosts, setHosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [labels, setLabels] = useState({ function: [], priority: [], type: [], application: [] , environment: []});
  const [selectfunction, setfunction] = useState("function");
  const [selectpriority, setpriority] = useState("priority");
  const [selecttype, settype] = useState("type");
  const [selectapplication, setapplication] = useState("application");
  const [selectenvironment, setenvironment] = useState("environment");
  const [selectedLabels, setSelectedLabels] = useState({});

  const API_URL_HOSTS = "http://sdn.yuntech.poc.com/ryu/hosts";
  const API_URL_LABEL = `http://sdn.yuntech.poc.com/datacenter/label/`;

  useEffect(() => {
    fetch(API_URL_HOSTS)
      .then((response) => response.json())
      .then((data) => {
        setHosts(data);
        setLoading(false);
      })
      .catch((error) => {
        console.error("Error fetching hosts data:", error);
        setLoading(false);
      });
  }, []);

  useEffect(() => {
    fetch(API_URL_LABEL + selectfunction)
      .then((response) => response.json())
      .then((data) => {
        setLabels((prevLabels) => ({
          ...prevLabels,
          [selectfunction]: data,
        }));
      })
      .catch((error) => {
        console.error("Error fetching label data:", error);
      });

    fetch(API_URL_LABEL + selectpriority)
      .then((response) => response.json())
      .then((data) => {
        setLabels((prevLabels) => ({
          ...prevLabels,
          [selectpriority]: data,
        }));
      })
      .catch((error) => {
        console.error("Error fetching label data:", error);
      });

    fetch(API_URL_LABEL + selecttype)
      .then((response) => response.json())
      .then((data) => {
        setLabels((prevLabels) => ({
          ...prevLabels,
          [selecttype]: data,
        }));
      })
      .catch((error) => {
        console.error("Error fetching label data:", error);
      });

    fetch(API_URL_LABEL + selectapplication)
      .then((response) => response.json())
      .then((data) => {
        setLabels((prevLabels) => ({
          ...prevLabels,
          [selectapplication]: data,
        }));
      })
      .catch((error) => {
        console.error("Error fetching label data:", error);
      });

      fetch(API_URL_LABEL + selectenvironment)
      .then((response) => response.json())
      .then((data) => {
        setLabels((prevLabels) => ({
          ...prevLabels,
          [selectenvironment]: data,
        }));
      })
      .catch((error) => {
        console.error("Error fetching label data:", error);
      });
  }, [selectfunction, selectpriority, selecttype, selectapplication , selectenvironment]);

  const handleLabelChange = (event, mac, category) => {
    const { value } = event.target;
    setSelectedLabels((prevSelectedLabels) => ({
      ...prevSelectedLabels,
      [mac]: {
        ...prevSelectedLabels[mac],
        [category]: value,
      },
    }));
  };

  const handleSubmit = (host) => {
    const labelsForHost = selectedLabels[host.mac] || {};

    const payload = {
      hostInfo: host,
      labels: labelsForHost,
    };
    console.log(payload);

    fetch("http://sdn.yuntech.poc.com/datacenter/submit_labels", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload),
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("Server response:", data);
        alert("Labels successfully submitted!");
      })
      .catch((error) => {
        console.error("Error submitting labels:", error);
        alert("Error submitting labels!");
      });
  };

  return (
    <Stack align="center" >
      <Heading> SDN 監控面板 </Heading>
      <Heading as="h3" size='lg' noOfLines={1} >主機資訊</Heading>

      {loading ? (
        <p style={{ textAlign: "center" }}>載入中...</p>
      ) : (
        <table className="tableStyle">
          <thead>
            <tr className="headerRowStyle">
              <th className="tableHeaderStyle">MAC 地址</th>
              <th className="tableHeaderStyle">IPv4 地址</th>
              <th className="tableHeaderStyle">IPv6 地址</th>
              <th className="tableHeaderStyle">連接埠名稱</th>
              <th className="tableHeaderStyle">Function</th>
              <th className="tableHeaderStyle">Priority</th>
              <th className="tableHeaderStyle">Type</th>
              <th className="tableHeaderStyle">Application</th>
              <th className="tableHeaderStyle">Environment</th>
              <th className="tableHeaderStyle" >送出</th>
            </tr>
          </thead>
          <tbody>
            {hosts.map((host, index) => (
              <tr key={index} style={index % 2 === 0 ? { backgroundColor: "#f9f9f9" } : { backgroundColor: "#fff" }}>
                <td className="tableCellStyle">{host.mac}</td>
                <td className="tableCellStyle">{host.ipv4.length > 0 ? host.ipv4.join(", ") : "N/A"}</td>
                <td className="tableCellStyle">{host.ipv6.length > 0 ? host.ipv6.join(", ") : "N/A"}</td>
                <td className="tableCellStyle">{host.port.name}</td>
                <td className="tableCellStyle">
                  <select
                    value={selectedLabels[host.mac]?.function || ""}
                    onChange={(e) => handleLabelChange(e, host.mac, "function")}
                    className="select-style"
                  >
                    <option value="">選擇標籤</option>
                    {labels[selectfunction]?.map((label, idx) => (
                      <option key={idx} value={label}>
                        {label}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="tableCellStyle">
                  <select
                    value={selectedLabels[host.mac]?.priority || ""}
                    onChange={(e) => handleLabelChange(e, host.mac, "priority")}
                    className="select-style"
                  >
                    <option value="">選擇標籤</option>
                    {labels[selectpriority]?.map((label, idx) => (
                      <option key={idx} value={label}>
                        {label}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="tableCellStyle">
                  <select
                    value={selectedLabels[host.mac]?.type || ""}
                    onChange={(e) => handleLabelChange(e, host.mac, "type")}
                    className="select-style"
                  >
                    <option value="">選擇標籤</option>
                    {labels[selecttype]?.map((label, idx) => (
                      <option key={idx} value={label}>
                        {label}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="tableCellStyle">
                  <select
                    value={selectedLabels[host.mac]?.application || ""}
                    onChange={(e) => handleLabelChange(e, host.mac, "application")}
                    className="select-style"                   
                  >
                    <option value="">選擇標籤</option>
                    {labels[selectapplication]?.map((label, idx) => (
                      <option key={idx} value={label}>
                        {label}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="tableCellStyle">
                  <select
                    value={selectedLabels[host.mac]?.environment || ""}
                    onChange={(e) => handleLabelChange(e, host.mac, "environment")}
                    className="select-style"                   
                  >
                    <option value="">選擇標籤</option>
                    {labels[selectenvironment]?.map((label, idx) => (
                      <option key={idx} value={label}>
                        {label}
                      </option>
                    ))}
                  </select>
                </td>
                <td className="tableCellStyle">
                  <button onClick={() => handleSubmit(host)} className="submit-button" >送出</button>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}


      <IntentTable  />
    </Stack>
  );
};

export default HostsTable;
