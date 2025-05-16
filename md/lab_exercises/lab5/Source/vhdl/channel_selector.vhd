library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity channel_selector is
    Port ( clk: in std_logic;
           btn: in std_logic;
           n_Reset: in std_logic;
           next_channel: out std_logic_vector(1 downto 0)
    );
end channel_selector;

architecture rtl of channel_selector is

    signal current_channel: std_logic_vector(1 downto 0) := "00";

begin

    selector: process (clk, n_Reset) is
    begin
        if (n_Reset = '0') then
            current_channel <= "00"; -- red
        elsif (rising_edge(clk) and btn='1') then
            if (current_channel = "00") then
                current_channel <= "01"; -- green
            elsif (current_channel = "01") then
                current_channel <= "10"; -- blue
            else
                current_channel <= "00"; -- red
            end if; -- select channel 
        end if; -- clk/rst
    end process; -- selector
    
    next_channel <= current_channel;

end rtl;
