import React, { useState, useEffect } from "react";
import { Heading, Button, Select, Box, Text, HStack , Input } from "@chakra-ui/react";
import "./HostsTable.css";

const API_URL_LABEL = `http://sdn.yuntech.poc.com/datacenter/label/`;

function IntentTable() {
    const [egress, setegress] = useState("");
    const [egress_list, setegress_list] = useState([]);  // 用來儲存 API 回傳的標籤項目
    const [egresstype, setegresstype] = useState("");

    const [ingress, setingress] = useState("");
    const [ingress_list, setingress_list] = useState([]); 
    const [ingresstype, setingresstype] = useState("");

    const [selectedProtocol, setSelectedProtocol] = useState("");  // 用來儲存選擇的關聯
    const [method, setMethod] = useState("");
    const [inputValue, setInputValue] = useState("");  // 用來儲存 Input 的值

    useEffect(() => {
        if (egress ) {
            
            fetch(`${API_URL_LABEL}${egress}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);  // 輸出API回傳的資料
                    setegress_list(data || []);  // 更新標籤項目
                    
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                });
        }
    }, [egress ]);  // 只有在 selectedLabel 改變時才會觸發

    useEffect(() => {
        if (ingress) {           
            fetch(`${API_URL_LABEL}${ingress}`)
                .then((response) => response.json())
                .then((data) => {
                    console.log(data);  // 輸出API回傳的資料
                    setingress_list(data || []);  // 更新標籤項目
                    
                })
                .catch((error) => {
                    console.error("Error fetching data:", error);
                });
        }
    }, [ingress]);  // 只有在 selectedLabel 改變時才會觸發

    useEffect(() => {
        if (selectedProtocol === "ICMP") {
            setInputValue("");
        }
    }, [selectedProtocol]);


    const handleProtocolChange = (event) => {
        setSelectedProtocol(event.target.value);  // 更新選中的關聯
    };
    
    const handleSubmit = () => {
        const data = {
            "method" : method,
            "egress" : egress,
            "egresstype" : egresstype,
            "protocol" : selectedProtocol,
            "port" : inputValue,
            "ingress" : ingress,
            "ingresstype" : ingresstype
        }
       
        console.log(data)
        // 應用意圖
        const POST_API = "http://sdn.yuntech.poc.com/datacenter/intent"
        fetch(POST_API, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(data),
        })
        .then((response) => {
            if (response.ok) {
                alert("Intent applied successfully");
            } else {
                alert("Error applying intent");
            }
        })
        .catch((error) => {
            console.error("Error:", error);
        });
    };


    return (
        <Box mt="5px" justifyItems="center">
            <Heading as="h3" size="lg" noOfLines={1}>
                意圖設定
            </Heading>

            <HStack m="5%" spacing="24px">
                <Box justifyItems="center">
                    <Text fontSize="xl" as="b">
                        方法
                    </Text>
                    <Select placeholder="Select option" onChange={(e) => { setMethod(e.target.value);}}>
                        <option value="allow"> allow </option>
                        <option value="deny"> deny </option>
                    </Select>
                </Box>
                <Box justifyItems="center">
                    <Text fontSize="xl" as="b">
                        標籤名稱
                    </Text>
                    <Select placeholder="Select option" onChange={(e) => { setegress(e.target.value)}}>
                        <option value="function"> Function </option>
                        <option value="application"> Application </option>
                        <option value="priority"> Priority </option>
                        <option value="type"> type </option>
                        <option value="environment"> environment </option>
                    </Select>
                </Box>
                <Box justifyItems="center">
                    <Text fontSize="xl" as="b">
                        標籤項目
                    </Text>
                    <Select placeholder="Select option" onChange={(e)=> { setegresstype(e.target.value)}}>
                        {egress_list.length > 0 ? (
                            egress_list.map((item, index) => (
                                <option key={index} value={item} >
                                    {item}
                                </option>
                            ))
                        ) : (
                            <option>No items available</option>
                        )}
                    </Select>
                </Box>
                <Box justifyItems="center">
                    <Text fontSize="xl" as="b">
                        關聯
                    </Text>
                    <Select placeholder="Select option" onChange={handleProtocolChange}>
                        <option value="ICMP"> ICMP </option>
                        <option value="TCP"> TCP </option>
                        <option value="UDP"> UDP </option>
                    </Select>
                </Box>
                {/* 當選擇 TCP 時顯示 Input */}
                {selectedProtocol === "TCP" && (
                    <Box justifyItems="center">
                        <Text fontSize="xl" as="b">
                            Protocol
                        </Text>
                        <br/>
                        <Input w="100px" value={inputValue} onChange={(e) => { setInputValue(e.target.value);}} />
                    </Box>
                )}
                <Box justifyItems="center">
                    <Text fontSize="xl" as="b">
                        標籤名稱
                    </Text>
                    <Select placeholder="Select option" onChange={(e) => { setingress(e.target.value)}}>
                        <option value="function"> Function </option>
                        <option value="application"> Application </option>
                        <option value="priority"> Priority </option>
                        <option value="type"> type </option>
                        <option value="environment"> environment </option>
                    </Select>
                </Box>
                <Box justifyItems="center">
                    <Text fontSize="xl" as="b">
                        標籤項目
                    </Text>
                    <Select placeholder="Select option" onChange={(e) => {setingresstype(e.target.value)}}>
                        {ingress_list.length > 0 ? (
                            ingress_list.map((item, index) => (
                                <option key={index} value={item} >
                                    {item}
                                </option>
                            ))
                        ) : (
                            <option>No items available</option>
                        )}
                    </Select>
                </Box>
                <Button onClick={handleSubmit}> 新增 </Button>
            </HStack>
        </Box>
    );
}

export default IntentTable;
