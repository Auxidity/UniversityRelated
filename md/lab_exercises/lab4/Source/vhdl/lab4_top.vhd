library IEEE;
use IEEE.STD_LOGIC_1164.ALL;

entity lab4_top is
    port (
        sysclk: in std_logic;
        btn: in std_logic_vector(1 downto 0);
        led5_r : out std_logic;
        led5_g : out std_logic;
        led5_b : out std_logic
	);
end lab4_top;

architecture rtl of lab4_top is

    component clock_divider is
    generic ( OUTPUT_FREQUENCY : integer := 1e3 );
	port (
		clk_in: in std_logic;
		n_Reset: in std_logic;
		clk_out: out std_logic
     );
    end component clock_divider;
    
    component button_pulser is
    generic ( DELAY : integer := 2000;
              INTERVAL : integer := 500
    );
    port (
        clk: in std_logic;
        btn: in std_logic;
        n_Reset: in std_logic;
        pulse: out std_logic
    );
    end component button_pulser;

    type rgb_state_t is (Red, Green, Blue);    
    signal rgb_state: rgb_state_t := Red;
    signal rgb_led_5: std_logic_vector(0 to 2) := "001";    
    signal n_Reset: std_logic;
    signal div_clk: std_logic; -- divided clock signal from clock divider
    signal pulse: std_logic;
 
    
begin
    
	n_Reset <= not btn(0);
    
    -- map signal "rgb_led_5" to actual output ports
    led5_r <= rgb_led_5(2);
    led5_g <= rgb_led_5(1);
    led5_b <= rgb_led_5(0);
    
    divider: clock_divider
    generic map (
        OUTPUT_FREQUENCY => 1e3
    )
    port map (
        clk_in => sysclk,
        n_Reset => n_Reset,
        clk_out => div_clk
    );
    
	pulser: button_pulser
	generic map (
	   DELAY => 2000,
	   INTERVAL => 500
	)   
	port map (
	   clk => div_clk,
	   btn => btn(1),
	   pulse => pulse,
	   n_Reset => n_Reset
	);
	
    rgb_selector: process (pulse, n_Reset) is
    begin
    
        if (n_Reset = '0') then -- check reset
            rgb_state <= Red;
            rgb_led_5 <= "001";

        elsif (pulse'event and pulse = '1') then
            case rgb_state is
                when Red =>
                    rgb_state <= Green;
                    rgb_led_5 <= "010";
                when Green =>
                    rgb_state <= Blue;
                    rgb_led_5 <= "100";
                when Blue =>
                    rgb_state <= Red;
                    rgb_led_5 <= "001";
                when others =>
                    rgb_state <= Red;
                    rgb_led_5 <= "001";
            end case;
       end if;
    
    end process rgb_selector;
	
end rtl;
