import { PieChart as RechartsPI, Pie, Cell, ResponsiveContainer, Tooltip, Legend } from 'recharts';

const COLORS = ['#09EF89', '#00A3FF', '#FF6B00', '#AC00FF', '#FFD600', '#FF0099', '#7CE2CB'];

const PieChart = ({ data, dataKey, nameKey }) => {
  return (
    <ResponsiveContainer width="100%" height={300}>
      <RechartsPI>
        <Pie
          data={data}
          cx="50%"
          cy="50%"
          labelLine={false}
          outerRadius={80}
          fill="#8884d8"
          dataKey={dataKey}
          nameKey={nameKey}
        >
          {data.map((entry, index) => (
            <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
          ))}
        </Pie>
        <Tooltip 
          contentStyle={{ backgroundColor: '#1E1E1E', borderColor: '#333' }} 
          itemStyle={{ color: '#FFF' }} 
        />
        <Legend layout="vertical" align="right" verticalAlign="middle" />
      </RechartsPI>
    </ResponsiveContainer>
  );
};

export default PieChart;
