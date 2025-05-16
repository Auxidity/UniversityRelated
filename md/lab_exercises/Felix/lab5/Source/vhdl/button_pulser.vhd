library IEEE;
use IEEE.STD_LOGIC_1164.ALL;
use IEEE.NUMERIC_STD.ALL;

entity button_pulser is
    Generic (
        DELAY : integer := 2000;
        INTERVAL : integer := 500    
    );
    Port ( clk : in std_logic;
           btn : in std_logic;
           n_Reset: in std_logic;
           pulse: out std_logic
    );
end button_pulser;


architecture rtl of button_pulser is

    type pulser_state_t is (Idle, Armed, Repeat);

    signal pulser_state: pulser_state_t := Idle;
    signal send_pulse: std_logic := '0';
    signal counter: integer range 0 to DELAY := 0;

    
begin

    button_pulser: process (clk, n_Reset) is
    begin
    
        if (n_Reset = '0') then -- check reset
            send_pulse <= '0';
            counter <= 0;
            pulser_state <= Idle;
            
        elsif clk'event and clk='1' then -- reset not activated       
            case pulser_state is
                
                when Idle =>
                    counter <= 0;    
                    if (btn = '1') then
                        send_pulse <= '1';
                        pulser_state <= Armed;
                    end if;
                
                when Armed =>
                    send_pulse <= '0';
                    if (btn = '1') then
                        if (counter < DELAY) then
                            counter <= counter + 1;
                        else
                            counter <= 0;
                            send_pulse <= '1';
                            pulser_state <= Repeat;
                        end if; -- counter                    
                    else -- btn was 0
                        pulser_state <= Idle;
                    end if; -- btn
                    
                when Repeat =>
                    
                    if (btn = '1') then
                    
                        if (counter < INTERVAL) then
                            counter <= counter + 1;
                            send_pulse <= '0';
                        else
                            send_pulse <= '1';
                            counter <= 0;
                        end if; -- counter
                    
                    else
                        send_pulse <= '0';
                        pulser_state <= Idle;
                    end if; -- btn
                   
                when others  => 
                    pulser_state <= Idle;
                
            end case;

        end if; -- reset / cases             

    end process button_pulser;
    
    pulse <= send_pulse;        
    

end rtl;
