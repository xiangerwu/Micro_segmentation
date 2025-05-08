import { memo } from 'react';
import { Box, Flex , Tag} from "@chakra-ui/react";
import { Handle, Position  } from '@xyflow/react';
 
function CustomNode({ data }) {
  const handleCount = data.count || 0;
  const nodeWidth = 100; // 與 Box 寬度一致
  
  return (
    <Box         
      background={"#fff"}
      borderRadius={"0%"}
      width={nodeWidth}
      height={50}
      display="flex"
      flexDirection="column"
      padding={"10px"}
      border="1px solid black"
      alignItems="center" justifyContent="center" >
        <Handle type="target" position={Position.Left} className='custom-handle' />
        <div>{data.label}</div>     
        <Flex align="center" justify="center" mt="5px" mb="5px">            
            <Tag size="sm" variant="solid" colorScheme="blue" mr="5px">{data.type}</Tag>       
        </Flex>
        <div className="resizer-node__handles">
          {Array.from({ length: handleCount }).map((_, idx) => {
            const spacing = nodeWidth / (handleCount + 1); // 平均分配位置
            const left = spacing * (idx + 1);
            return (
              <Handle                
                id={`h-${idx}`}
                type="source"
                position={Position.Bottom}
                style={{ left }}
                className="resizer-node__handle custom-handle"
              />
            );
          })}
        </div>
    </Box>
  );
}
 
export default memo(CustomNode);