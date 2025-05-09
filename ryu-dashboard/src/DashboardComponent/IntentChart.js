import React, { useEffect, useRef } from "react";
import {
  ReactFlow,
  MarkerType,
  useNodesState,
  useEdgesState,
  Background,
  Position
} from "@xyflow/react";
import "@xyflow/react/dist/style.css";
import CustomNode from "./CustomNode";

import { Tag , Flex , Stack , Heading } from "@chakra-ui/react";
import react from "react";

const MIN_DISTANCE = 150;

const nodeTypes = {
  custom: CustomNode,
};

const generatePosition = (index) => {
    const x = index % 2 === 0 ? 300 : 600; // 偶數索引在 x = 300，奇數索引在 x = 600
    const y = Math.floor(index / 2) * 100; // 每行 y 值遞增 100
  
    return { x, y };
  };


function IntentChart() {
  
  const [nodes, setNodes, onNodesChange] = useNodesState([]);
  const [edges, setEdges, onEdgesChange] = useEdgesState([]);
  const edgeCache = useRef([]); // 用於緩存邊的 ID
  const initializedRef = useRef(false); // 用於檢查是否已經初始化過

  useEffect(()=>{
    const loadData = async () => {
        
          // 讀取 nodes.json          
          const Response = await fetch('http://sdn.yuntech.poc.com/datacenter/dsl')
          const ResJson = await Response.json();
          let idx = 0 ;
          
          // 將 nodes.json 中的每個節點轉換為 React Flow 的節點格式
          const updatedNodes = ResJson.nodes.map((node, index) => ({
            id: node.id,
            type: 'custom', // 使用自定義的節點類型
            position: generatePosition(index), // 動態生成位置
            data: { type: node.type, label: node.label , count: node.count},           
          }));
  
          // 更新 nodes 狀態
          setNodes(updatedNodes);

          
          // edge的部分
          const updatedEdges = ResJson.edges.map(edge => ({
            id: edge.id,
            source: edge.source,
            target: edge.target,
            label: edge.label,            
            animated: true, 
            action : edge.action,
            sourceHandle: "h-" + (idx++),
            style: { stroke: edge.action == "deny" ? "red" : "teal" }, 
            markerEnd: { type: MarkerType.ArrowClosed },
          }));
          setEdges(updatedEdges);
          //edgeCache.current = updatedEdges;          
    }

    loadData();

  },[setNodes,setEdges])

  // 等nodes 初始化完成後，再設定edges
  const onInit = (reactFlowInstance) => {
    if (!initializedRef.current) {
      initializedRef.current = true;
      setEdges(edgeCache.current);
    }
  };

  return (
    <Stack align="center" ml = "10%" mr="10%" w="80%" h="1000px">
       <Heading> 策略可達圖 </Heading>
      <ReactFlow
        nodes={nodes}
        edges={edges}
        onInit={onInit}
        onNodesChange={onNodesChange}
        onEdgesChange={onEdgesChange}
        nodeTypes={nodeTypes}        
        style={{ backgroundColor: "#F7F9FB" }}
        fitView
      >
        <Background />
      </ReactFlow>
    </Stack>
  );
}

export default IntentChart;
