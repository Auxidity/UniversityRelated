library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity clock_divider is
    Generic (
        OUTPUT_FREQUENCY : integer := 1e3 -- default 1 kHz       
    );
    Port ( clk_in : in std_logic;
           n_Reset: in std_logic;
           clk_out : out std_logic
    );
end clock_divider;

architecture rtl of clock_divider is

    constant clock_ratio : integer := 125e6 / OUTPUT_FREQUENCY;
    constant divide_ratio : integer := (clock_ratio - 1) / 2;    
    signal counter: integer range 0 to clock_ratio := 0;


begin
        
    counter1: process (clk_in, n_Reset) is
    begin
        if (n_Reset = '0') then
            counter <= 0;
            clk_out <= '0';
            
        elsif clk_in'event and clk_in='1' then        
            if counter >= clock_ratio then         
                counter <= 0;
            else
                counter <= counter + 1;
            end if;
            
            -- Toggle output clock if the divide ratio has been reached
            if counter >= divide_ratio then
                clk_out <= '1';
            else
                clk_out <= '0';
            end if;
                
        end if; -- clk/rst
    end process counter1;

end rtl;
