library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;


entity intensity is
    Generic (
        RGB_BITS: integer       
    );
    Port ( clk: in std_logic;
           n_Reset: in std_logic;
           channel: in std_logic_vector(1 downto 0);
           increase: in std_logic;
           decrease: in std_logic;
           new_red: out std_logic_vector(RGB_BITS - 1 downto 0);
           new_green: out std_logic_vector(RGB_BITS - 1 downto 0);
           new_blue: out std_logic_vector(RGB_BITS - 1 downto 0)           
    );
end intensity;

architecture rtl of intensity is
    constant max_value: integer := 2**RGB_BITS-1;
    signal current_red: integer range 0 to max_value := 0;
    signal current_green: integer range 0 to max_value := 0;
    signal current_blue: integer range 0 to max_value := 0;
    
begin

    intensity: process (clk, n_Reset) is
    begin
        if (n_Reset = '0') then
            current_red <= 0;
            current_green <= 0;
            current_blue <= 0;
        
        elsif (rising_edge(clk) and (increase='1' or decrease='1')) then
            if (channel = "00") then
                if (increase = '1' and current_red + 1 <= max_value) then            
                    current_red <= current_red + 1;
                elsif (decrease = '1' and current_red - 1 >= 0) then
                    current_red <= current_red - 1;
                end if; -- channel "00"
                
            elsif (channel = "01") then
                if (increase = '1' and current_green + 1 <= max_value) then            
                    current_green <= current_green + 1;
                elsif (decrease = '1' and current_green - 1 >= 0) then
                    current_green <= current_green - 1;
                end if; -- channel "01"
                                
            elsif (channel = "10") then
                if (increase = '1' and current_blue + 1 <= max_value) then            
                    current_blue <= current_blue + 1;
                elsif (decrease = '1' and current_blue - 1 >= 0) then
                    current_blue <= current_blue - 1;
                end if; -- channel "10"

            end if; -- rising edge / adjust color
        end if; -- clk/rst

    end process intensity;

    new_red <= std_logic_vector(to_unsigned(current_red, RGB_BITS));
    new_green <= std_logic_vector(to_unsigned(current_green, RGB_BITS));
    new_blue <= std_logic_vector(to_unsigned(current_blue, RGB_BITS));

        
end rtl;
