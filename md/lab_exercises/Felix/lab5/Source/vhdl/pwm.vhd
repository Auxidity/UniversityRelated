library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity pwm is
    Generic (
        PWM_RESOLUTION : integer       
    );
    Port ( clk : in std_logic;
           n_Reset : in std_logic;
           pwm_ratio : in std_logic_vector(PWM_RESOLUTION - 1 downto 0);
           pwm_out : out std_logic
    );
end pwm;

architecture rtl of pwm is

    constant full_width : integer := 2**PWM_RESOLUTION - 2; -- minus 2, because we use range 0-255, and zero is omitted in the counter 
    signal counter : integer range 0 to full_width := 0;
    signal toggle_point : integer range 0 to full_width;

begin

    toggle_point <= to_integer(unsigned(pwm_ratio));

    pwm: process (clk, n_Reset) is
    begin
        if (n_Reset = '0') then
            pwm_out <= '0';
            counter <= 0;
        
        elsif (rising_edge(clk)) then            
            if toggle_point = 0 then
                pwm_out <= '0';
            else
        
                if (counter >= full_width) then 
                    counter <= 0;
                else
                    counter <= counter + 1;
                end if; --counter
    
                if (counter >= toggle_point) then
                    pwm_out <= '0';                
                else
                    pwm_out <= '1';
                end if; -- pwm_out
            end if; --pulse toggler
        end if; --clk/rst
    end process pwm;

end rtl;
